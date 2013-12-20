#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Copyright (c) 2013, Quincy Lam 
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of  nor the names of its contributors may be used to 
   endorse or promote products derived from this software without specific 
   prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE. 
"""
import argparse
import re

class Table:
	"""	Represents a table	"""

	def __init__(self):
		self.rows = []
		self.cols = []

	def from2DList(self, twodArray):
		""" Constructs a Table from a 2-d list, which should be a list of rows, all of the same length """
		self.rows = twodArray
		self.cols = [ [row[n] for row in twodArray] for n in range(len(twodArray[0]))]

	def fromFile(self, filename, delim='\t'):
		""" Constructs a Table from a delim-SV. Make sure the headings contain no newlines. """
		a = open(filename, "r")
		b = [line.split(delim) for line in a.readlines()]
		a.close()
		self.from2DList(b)

	rows = []
	""" List of rows in the table"""

	cols = []
	""" List of colums in the table"""

	size = 3
	
	def str(self):
		""" Returns a LaTeX table formatted as follows:
		- 40% grey borders
		- perimeter 2¼ pt
		- inner ¾ pt
		- centred small caps headings
		- align the ±
		- no less than 10pt font
		"""

		rows = list(self.rows)
		cols = list(self.cols)

		alignmentChars = [self._findAlignmentChar(col) for col in cols]
		maxDecimalPlaces = [self._findMaxDecimalPlaces(col) for col in cols]

		head = r"\begin{tabu} to " + str(self.size) + r"in {|"
		for i,char in enumerate(alignmentChars):
			if char == "":
				head += "X[c]"
			else:
				# head += "X[D{{{0}}}{{{0}}}{{".format(char) + str(maxDecimalPlaces[i]) + "}]"
				head += "X[r]X[l]"
			head += "|"

		head += r"} \tabucline[tblOuter]{-}"

		body = ""

		variablesRow = "&".join([r"\multicolumn{{{0}}}{{{2}}}{{{1}}}".format(self._getWidthInColumns([heading]), self._smallCapsHeading(heading[:self._locateUnit(heading)]).strip(), self._getAlignmentString(i, len(rows[0]) - 1) ) for i,heading in enumerate(rows[0])]) + r"\\" + "\n"
		body += variablesRow

		unitsRow = "&".join([r"\multicolumn{{{0}}}{{{2}}}{{{1}}}".format(self._getWidthInColumns([heading]), heading[self._locateUnit(heading):], self._getAlignmentString(i, len(rows[0]) - 1) ) for i,heading in enumerate(rows[0])]) + r"\\ \tabucline{-}" + "\n"
		body += unitsRow

		body += (r"\\ \tabucline{-}" + "\n").join(["&".join(row) for row in [self._divideCells(row, alignmentChars) for row in rows[1:]] ])
		
		tail = r"\\ \tabucline[tblOuter]{-} \tabuphantomline" + "\n" + r"\end{tabu}"

		return head + '\n' + body + tail

	def _findAlignmentChar(self, col):
		""" Finds out how to align the values in this column by reading the units in the last parantheses. 

			If this is the Index column, centre things normally.

			If there is a constant uncertainty, then there must not be uncertainties in the values, so centre them by decimal point. If the constant uncertainty has no decimal point (i.e. exceeds 0), then the values have no decimal points, so centre normally.

			If there isn't an uncertainty, then there must be uncertainties in the values, so centre them by the ±.

			If there are no units, then centre by ±."""

		head = col[0]
		if head == "Index":
			return ""
		try:
			lastParentheses = re.search(r"\(([^()]+)\)$",head).group(1)
			if "±" in lastParentheses:
				if "." in lastParentheses:
					return "."
				else:
					return ""
			else:
				return "±"
		except (AttributeError, IndexError):
			return "±"

	def _findMaxDecimalPlaces(self, col):
		""" Finds out the most decimal places after the ± or the decimal point there are in the column"""
		ret = 0
		for cell in col[1:]:
			if "±" in cell:
				if len(cell.split("±")[1]) > ret:
					ret = len(cell.split("±")[1])
			elif "." in cell:
				if len(cell.split(".")[1]) > ret:
					ret = len(cell.split(".")[1])
		return ret

	def _insertNewlineBeforeUnits(self, heading):
		""" Finds the last set of parentheses, which contain the units, and inserts \newline"""
		if len(re.findall(r"\(.*?\)",heading)) >= 2:
			m = re.search(r"\([^()]*\)$",heading)
			return heading[:m.start()] + r"\newline" + heading[m.start():]
		return heading

	def _smallCapsHeading(self,heading):
		""" Puts small caps on the field name """
		if heading.find("(") != -1:
			return r"\textsc{" + heading[:heading.find("(") - 1] + r"} " + heading[heading.find("("):]
		return r"\textsc{" + heading + r"}"

	def _getWidthInColumns(self, col):
		""" Determines whether the things under this heading will require 1 or 2 columns (is there a decimal point/plusminus?) """
		# If there is no constant uncertainty, then each value must have uncertainties
		if self._findAlignmentChar(col) == "":
			return 1
		return 2

	def _divideCells(self, row, seps):
		""" Once in each cell in row, splits the cell into 2 cells with sep going to the later cell """
		ret = []
		for i,(cell,sep) in enumerate(zip(row, seps)):
			if sep != "":
				# [:-1] the right border must be removed because this is only the first part of a mantissa uncertainty pair
				# @{...} this shifts the mantissa over. For some reason, the decimal point or the ± will already be in the centre, so we cannot touch its spacing.
				ret.append(r"\multicolumn{{1}}{{{1}}}{{{0}}}".format(cell.split(sep)[0], self._getAlignmentString(i, len(row) - 1, alignment='r')[:-1] + "@{}"))
				ret.append(r"\multicolumn{{1}}{{{1}}}{{{0}}}".format(sep + cell.split(sep)[1], "@{}" + self._getAlignmentString(i, len(row) - 1, alignment='l')))
			else:
				ret.append(r"\multicolumn{{1}}{{{1}}}{{{0}}}".format(cell, self._getAlignmentString(i, len(row) - 1)))
		return ret

	def _locateUnit(self, cell):
		""" Returns the index of the parenthesis that surrounds the constant uncertainty and the unit, if it exists """
		try:
			return re.search(r"(\()±?[^()]+\)$", cell).start(1)
		except AttributeError:
			return len(cell)

	def _getAlignmentString(self, i, maxI, alignment='c'):
		""" Returns an alignment string with thicker borders if the cell is an exterior one """
		return ("|[tblOuter]" + alignment + "|") if i == 0 else (alignment + "|[tblOuter]") if i == maxI and alignment !='r' else (alignment + "|")

def main():
	parser = argparse.ArgumentParser(description='Generate LaTeX table(s) formatted for vB standards.')
	parser.add_argument('tsvs', metavar='FILE', nargs='+', help='filenames of tab-separated values representing tables to be formatted')
	parser.add_argument('--wide', help='Make this table 6.5in wide instead of 3in', action='store_true')

	args = parser.parse_args()

	t = Table()
	t.size = 6.5 if args.wide else 3

	for filename in args.tsvs:
		t.fromFile(filename)
		print t.str()
		

if __name__ == "__main__":
	main()

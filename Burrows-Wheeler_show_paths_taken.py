class Burrows_Wheeler:

	def __init__(self, text):
		assert len(text)>0,"No text"
		self.text = text
		self.bwm, self.bwt = self.BWT(text)
		self.C_table, self.C_alphabet = self.Make_C_table()
		self.Occ_table, self.Occ_alphabet = self.Make_Occ_table()
		self.suffix_index = self.make_suffix_array_index()


	def get_row_numbers(self, c):
		start_row = self.C_table[c]
		current_index = self.Occ_alphabet.index(c)
		if current_index == len(self.Occ_alphabet) - 1:  # we are at the last char in the Occ table
			Occ_last_row = len(self.Occ_table) - 1
			Occ_char_column = self.Occ_alphabet.index(c)
			Occ_entry = self.Occ_table[Occ_last_row][Occ_char_column]
			end_row = start_row + Occ_entry
		else:
			end_row = self.C_table[self.Occ_alphabet[current_index + 1]]
		return (start_row, end_row)


	def BWT(self, text):
		if len(text) < 2:
			return (0, 0)
		if text[-1:] != '$':
			text += '$'

		array = [list(text)] * len(text)
		for i in range(1, len(text)):
			array[i] = array[i - 1][-1:] + array[i - 1][:-1]
		bwm = sorted(array)
		bwt = [i[-1] for i in bwm]
		print("bwt=",bwt)
		return (bwm, bwt)


	def Make_C_table(self):
		first_column = [str(i[0]) for i in self.bwm]  # get irst column as a list of characters
		alphabet = sorted(set(first_column))  # get only the unique symbols, sorted
		c_table = {alphabet[0]: 0}
		symbols_above = 0
		for i in range(1, len(alphabet)):  # add symbols and number chars above it to dict
			symbols_above += first_column.count(alphabet[i - 1])
			c_table[alphabet[i]] = symbols_above
		return c_table, alphabet


	def Make_Occ_table(self):
		alphabet = sorted(set(self.bwt))
		tally_row = [0] * len(alphabet)
		occ_table = []
		for i in range(0, len(self.bwt)):
			tally_row[alphabet.index(self.bwt[i])] += 1
			occ_table.append(tally_row.copy())
		return occ_table, alphabet


	def make_suffix_array_index(self):
		suffix_index = []
		for r in self.bwm:
			suffix_index.append(len(self.bwm) - r.index('$') - 1)
		return suffix_index


	def search_bw(self, pattern):
		pattern_rev = pattern[::-1]

		start, end = self.get_row_numbers(pattern[0])
		row_to_read = [0] * (end - start)
		print('The symbol we are looking for is',pattern[0])
		print('Looking at the C-table, we must look from row',start,"to row",end-1)
		for i in range(start, end):
			row_to_read[i - start] = i
		symbol = 0
		while symbol < len(pattern) - 1 and len(row_to_read) > 0:
			i = 0
			symbol += 1
			while i < len(row_to_read):
				if self.bwt[row_to_read[i]] == pattern[symbol]:
					my_occ = self.C_table[self.bwt[row_to_read[i]]]
					my_symbol = self.bwt[row_to_read[i]]
					my_rank = self.Occ_table[row_to_read[i]][self.Occ_alphabet.index(pattern[symbol])] - 1
					my_row = row_to_read[i]
					row_to_read[i] = self.C_table[self.bwt[row_to_read[i]]] + self.Occ_table[row_to_read[i]][self.Occ_alphabet.index(pattern[symbol])] - 1
					print("The symbol at row", my_row, "is", my_symbol, "and the rank is",my_rank,"so we look in row", my_occ, "+",my_rank, "=",my_occ+my_rank)

					i += 1
				else:
					print("The symbol at row",row_to_read[i],"is",self.bwt[row_to_read[i]],"<- we stop following this track")
					del row_to_read[i]
		matches = []
		for i in row_to_read:
			print("The suffix at row",i,"is",self.suffix_index[i])
			matches.append(self.suffix_index[i])
		print("The pattern",pattern,"thus occurs in the text",len(matches),"times, at positions",sorted(matches))
		return sorted(matches)

#---------------------------------------------------------------------------------------------------------------------

# This program shows in detail the path taken to try and find a pattern in text
# You can use this to run through examples to make sure that you understand
# the principle

text = 'GACACTCACG$' #'GCACTCACAG$'
pattern = 'CAA'

bw = Burrows_Wheeler(text)
bw.search_bw(pattern)



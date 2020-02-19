import requests
import json
from googletrans import Translator

class TranslationUtil():
	def __init__(self):
		self.translator = Translator()

	def translate(self,word,mode, Iter=True):	#translates a word from farsi to english or vise-versa
		if mode == "en_fa":
			translated = self.translator.translate(word, dest="fa")
			return translated.text
		else:
			translated = self.translator.translate(word)
			trans_list = [translated.text]
			if translated.extra_data['possible-translations'] != None:
				tmp = translated.extra_data['possible-translations'][0][2]
				for elem in tmp:
					trans_list.append(elem[0])
			if translated.extra_data['see-also'] != None and Iter:
				trans_list.extend(self.translate(translated.extra_data['see-also'][0][0],"fa_en",True))
			return trans_list

	def unify(self, L):	# takes a list and makes its elements unique (e.g. no similars)
		L_copy = []
		for elem in L:
			if elem not in L_copy:
				L_copy.append(elem)
		return L_copy
	
	def clear(self,word):	#removes all non alphanumeric chars from begining and end of str
		fwd_cnt = 0
		while(fwd_cnt < len(word) and word[fwd_cnt].isalnum() == False):
			fwd_cnt += 1
		bwd_cnt = len(word)
		while(bwd_cnt > 0 and word[bwd_cnt - 1].isalnum() == False):
			bwd_cnt-=1

		if bwd_cnt < fwd_cnt:
			return None

		return word[fwd_cnt:bwd_cnt]

import wikipedia
import operator
import numpy as np
import threading
import requests
import json

from TranslationUtil import TranslationUtil as translator

class BrainStorm(threading.Thread):
	def __init__(self, persian_keyword, possible_labels, bag_of_words):
		threading.Thread.__init__(self)
		self.persian_keyword = persian_keyword
		self.possible_labels = possible_labels
		self.Translator = translator()
		self.bag_of_words = bag_of_words

 
	def clear(self,word):	#removes all non alphanumeric chars from begining and end of str
		fwd_cnt = 0
		while(fwd_cnt < len(word) and word[fwd_cnt].isalnum() == False):
			fwd_cnt += 1
		bwd_cnt = len(word)
		while(bwd_cnt > -1 and word[bwd_cnt - 1].isalnum() == False):
			bwd_cnt-=1

		if bwd_cnt < fwd_cnt:
			return None

		return word[fwd_cnt:bwd_cnt]

	def unify(self, L):	# takes a list and makes its elements unique (e.g. no similars)
		L_copy = []
		for elem in L:
			if elem not in L_copy:
				L_copy.append(elem)
		return L_copy

	def translate(self,word,mode):	#translates a word from farsi to english or vise-versa
		response = self.Translator.translate(word,mode)
		resp = response['tr']['alignments'][0][0][2]
		res_list = []
		for res in resp:
			res[0] = res[0].lower()
			res[0] = self.clear(res[0])
			if res[0] != None:
				res_list.append(res[0])
		
		res_list = self.unify(res_list)
		#returns the exact translation and possible similar translations
		return [ response['tr']['base'][0][1].lower(), res_list]

	def run(self):
		local_bag_of_words = []
		local_bag_of_words.extend(self.translate(self.persian_keyword,"fa_en")[1])
		for word in local_bag_of_words:
			new_list = wikipedia.search(word, results= 50)
			self.possible_labels.extend(new_list)
		self.bag_of_words.extend(local_bag_of_words)

class LabelMatching(threading.Thread):
	def __init__(self, label, bag_of_words, match_score):
		threading.Thread.__init__(self)
		self.label = label
		self.bag_of_words = bag_of_words
		self.match_score = match_score
	
	def run(self):
		try:
			label_description = wikipedia.summary(self.label)
			label_description = label_description.lower()
			cnt = 0;
			for word in self.bag_of_words:
				if word in label_description:
					cnt += 1
			self.match_score.append([self.label, cnt])
		except:
			pass

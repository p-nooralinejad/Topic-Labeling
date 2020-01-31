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
	
	def translate(self,word,mode):	#translates a word from farsi to english or vise-versa
		response = self.Translator.translate(word,mode)
		resp = response['tr']['alignments'][0][0][2]
		res_list = []
		for res in resp:
			res[0] = res[0].lower()
			res[0] = self.Translator.clear(res[0])
			if res[0] != None:
				res_list.append(res[0])
		
		res_list = self.Translator.unify(res_list)
		#returns the exact translation and possible similar translations
		return [ response['tr']['base'][0][1].lower(), res_list]

	def run(self):
		local_bag_of_words = []
		local_bag_of_words.extend(self.translate(self.persian_keyword,"fa_en")[1])
		for word in local_bag_of_words:
			try:
				new_list = wikipedia.search(word, results= 45)
				self.possible_labels.extend(new_list)
			except:
				pass
		valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		for word in local_bag_of_words:
			if word.isalnum() and len(word) > 1 and any(valid in word for valid in valid_chars):
				self.bag_of_words.append(word)

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
			label_description = label_description.split()
			cnt = 0;
			for word in self.bag_of_words:
				if any(word in phrase for phrase in label_description):
					cnt += 1
				if word in self.label.lower():
					cnt += 3
			self.match_score.append([self.label, cnt])
		except:
			pass

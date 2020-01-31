import wikipedia
import operator
import numpy as np
import threading
import requests
import json
from Topic import BrainStorm as topic_brain_storm
from Topic import LabelMatching as topic_label_matching
from TranslationUtil import TranslationUtil as translator

class TopicLabeling():
	def __init__(self, persian_words):
		self.persian_words = persian_words
		self.bag_of_words = []
		self.brain_storm_thread_pool = []
		self.possible_labels = []
		self.label_score = {}
		self.matching_score = []
		self.label_matching_thread_pool = []
		self.soft_persian = {}
		self.Translator = translator()

	def soft_and_sort(self, dictionary):
		denom = 0
		for key in dictionary.keys():
			denom += np.exp(dictionary[key])

		dic = {}
		for key in dictionary.keys():
			dictionary[key] = np.exp(dictionary[key]) / denom
			dic[key] = dictionary[key]

		sorted_d = dict( sorted(dic.items(), key=operator.itemgetter(1),reverse=True))
		final = {}
		cnt = 0
		for k in sorted_d.keys():
			final[k] = sorted_d[k]
			cnt += 1
			if cnt == 10:
				break
		return final

	def translate(self,word,mode):	#translates a word from farsi to english or vise-versa
		response = self.Translator.translate(word,mode)
		return response['tr']['base'][0][1].lower()

	def assign_label(self):
		print("Initiating topic labeling for wordset:", self.persian_words)
		for i in range(len(self.persian_words)):	
			self.persian_words[i] = self.persian_words[i][:-1]
			new_thread = topic_brain_storm(self.persian_words[i], self.possible_labels, self.bag_of_words)
			self.brain_storm_thread_pool.append(new_thread)
			new_thread.start()

		#wait for brainstorming to finish
		for thread in self.brain_storm_thread_pool:	
			thread.join()
		print("Translation and Label brainstorming finished, evaluating each label")
		self.bag_of_words = self.Translator.unify(self.bag_of_words)
		#initialize scores
		for possible_label in self.possible_labels:
			self.label_score[possible_label] = 0

		#calculate similarty of each page to our keywords
		for possible_label in self.possible_labels:
			try:
				new_thread = topic_label_matching(possible_label, self.bag_of_words, self.matching_score)	
				new_thread.start()
				self.label_matching_thread_pool.append(new_thread)
				
			except Exception as e:
				pass

		#wait for matching to finish
		for t in self.label_matching_thread_pool:
			t.join()

		print("Label evaluation finished")
		#accumulate scores
		for elem in self.matching_score:
			self.label_score[elem[0]] += elem[1]

		#softmax and report possible topics
		soft = self.soft_and_sort(self.label_score)	
		topic_labels = []
		for k in soft.keys():
			#print(k, self.translate(k,'en_fa'))
			topic_labels.append((k , self.translate(k,'en_fa')))
		
		return topic_labels

import wikipedia
import operator
import numpy as np
import threading
import requests
import json

class BrainStorm(threading.Thread):
	def __init__(self, persian_keyword, possible_labels, bag_of_words):
		threading.Thread.__init__(self)
		self.persian_keyword = persian_keyword
		self.faraazin_header = {"Connection": "keep-alive",\
			 "Accept": "application/json, text/plain, */*", \
			 "Authorization": "Bearer undefined", \
			 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",\
			 "Content-Type": "application/json;charset=UTF-8", \
			 "Origin": "https://www.faraazin.ir", \
			 "Sec-Fetch-Site": "same-origin", \
			 "Sec-Fetch-Mode": "cors",\
			 "Referer": "https://www.faraazin.ir/?q=%D8%AE%D9%88%D8%AF%DA%A9%D8%A7%D8%B1",\
			 "Accept-Encoding": "gzip, deflate, br",\
			 "Accept-Language": "en-US,en;q=0.9",\
			 "Cookie": "_ga=GA1.2.1845074656.1579521051; G_ENABLED_IDPS=google; _mh=%22%2C19%22; _gid=GA1.2.673830774.1579615715; G_AUTHUSER_H=0"\
		}
		self.possible_labels = possible_labels
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
		payload = {"text":word,"mode": mode}
		r = requests.post("https://www.faraazin.ir/api/translate", data=json.dumps(payload), headers=self.faraazin_header)
		response = json.loads(r.text)
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
		print(self.persian_keyword)
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
		label_description = wikipedia.summary(self.label)
		label_description = label_description.lower()
		cnt = 0;
		for word in self.bag_of_words:
			if word in label_description:
				cnt += 1
		self.match_score.append([self.label, cnt])

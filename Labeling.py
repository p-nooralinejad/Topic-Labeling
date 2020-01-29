
import wikipedia
import operator
import numpy as np
import threading
import requests
import json
from Topic import BrainStorm as topic_brain_storm
from Topic import LabelMatching as topic_label_matching

def soft_and_sort(dictionary):
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


def translate(word,mode):	#translates a word from farsi to english or vise-versa
	payload = {"text":word,"mode": mode}
	faraazin_header = {"Connection": "keep-alive",\
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
	r = requests.post("https://www.faraazin.ir/api/translate", data=json.dumps(payload), headers=faraazin_header)
	response = json.loads(r.text)
	return response['tr']['base'][0][1].lower()

#Load File
print('enter file address: ')
file_name = input()
File = open(file_name, 'r')
persian_words = File.readlines()
File.close()

#initialize
bag_of_words = []
brain_storm_thread_pool = []
possible_labels = []
label_score = {}
matching_score = []
label_matching_thread_pool = []
soft_persian = {}

#translate keywords extracted by LDA and gather related topics
for i in range(len(persian_words)):	
	persian_words[i] = persian_words[i][:-1]
	new_thread = topic_brain_storm(persian_words[i], possible_labels, bag_of_words)
	brain_storm_thread_pool.append(new_thread)
	new_thread.start()

#wait for brainstorming to finish
for thread in brain_storm_thread_pool:	
	thread.join()

#initialize scores
for possible_label in possible_labels:
	label_score[possible_label] = 0

#calculate similarty of each page to our keywords
for possible_label in possible_labels:
	try:
		new_thread = topic_label_matching(possible_label, bag_of_words, matching_score)	
		new_thread.start()
		label_matching_thread_pool.append(new_thread)
		print(possible_label)
	except Exception as e:
		pass

#wait for matching to finish
for t in label_matching_thread_pool:
	t.join()

#accumulate scores
for elem in matching_score:
	label_score[elem[0]] += elem[1]

#softmax and report possible topics
soft = soft_and_sort(label_score)	

for k in soft.keys():
	soft_persian[translate(k,'en_fa')] = soft[k]

print('--------------------------------------------')
for k in soft_persian.keys():
	print(k)

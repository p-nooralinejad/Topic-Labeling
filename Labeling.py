import wikipedia
import operator
import numpy as np
import threading
import requests
import json

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


#Load words
file_name = input('enter file name: ')
threadLock = threading.Lock()
File = open(file_name, 'r')
file_bag_of_word = File.readlines()
File.close()

#default header of faraazin API
headers = {"Connection": "keep-alive",\
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
			 "Cookie": "_ga=GA1.2.1845074656.1579521051; G_ENABLED_IDPS=google; _mh=%22%2C19%22; _gid=GA1.2.673830774.1579615715; G_AUTHUSER_H=0"}

def clear(word):	#removes all non alphanumeric chars from begining and end of str
	fwd_cnt = 0
	while(fwd_cnt < len(word) and word[fwd_cnt].isalnum() == False):
		fwd_cnt += 1
	bwd_cnt = len(word)
	while(bwd_cnt > -1 and word[bwd_cnt - 1].isalnum() == False):
		bwd_cnt-=1

	if bwd_cnt < fwd_cnt:
		return None

	return word[fwd_cnt:bwd_cnt]

def unify(L):	# takes a list and makes its elements unique (e.g. no similars)
	L_copy = []
	for elem in L:
		if elem not in L_copy:
			L_copy.append(elem)
	return L_copy

def translate(word,mode):	#translates a word from farsi to english or vise-versa
	payload = {"text":word,"mode": mode}
	r = requests.post("https://www.faraazin.ir/api/translate", data=json.dumps(payload), headers=headers)
	response = json.loads(r.text)
	resp = response['tr']['alignments'][0][0][2]
	res_list = []
	for res in resp:
		res[0] = res[0].lower()
		res[0] = clear(res[0])
		if res[0] != None:
			res_list.append(res[0])
	
	res_list = unify(res_list)
	#returns the exact translation and possible similar translations
	return [ response['tr']['base'][0][1].lower(), res_list]

bag_of_word = []
for i in range(len(file_bag_of_word)):	#translate keywords extracted by LDA
	file_bag_of_word[i] = file_bag_of_word[i][:-1]
	print(file_bag_of_word[i])
	bag_of_word.extend(translate(file_bag_of_word[i],'fa_en')[1])

#extract possible labels
possible_labels = []
for word in bag_of_word:	#search for similar pages in wikipedia based on keywords
	print(word)
	new_list = wikipedia.search(word, results= 50)
	possible_labels.extend(new_list)
#evaluate labels

label_score = {}
thread_explored_data = []

class data_extraction_thread (threading.Thread):
	def __init__(self, label):
		threading.Thread.__init__(self)
		self.label = label

	def run(self):
		label_description = wikipedia.summary(self.label)
		label_description = label_description.lower()
		cnt = 0;
		for word in bag_of_word:
			if word in label_description:
				cnt += 1
		thread_explored_data.append( [self.label, cnt])
				
cnt = 0

threads  = []

for possible_label in possible_labels:
	try:
		new_thread = data_extraction_thread(possible_label)	#calculate similarty of a page to our keywords
		cnt += 1
		new_thread.start()
		threads.append(new_thread)
		print(possible_label)
	except Exception as e:
		pass

for t in threads:
	t.join()

for possible_label in possible_labels:
	label_score[possible_label] = 0

for elem in thread_explored_data:
	label_score[elem[0]] += elem[1]

soft = soft_and_sort(label_score)	#softmax and report possible topics
soft_persian = {}
for k in soft.keys():
	soft_persian[translate(k,'en_fa')[0]] = soft[k]

print(soft_persian)

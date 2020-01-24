import wikipedia
import operator
import numpy as np
import threading

def soft_and_sort(dictionary):
	denom = 0
	for key in dictionary.keys():
		denom += np.exp(dictionary[key])

	dic = {}
	for key in dictionary.keys():
		dictionary[key] = np.exp(dictionary[key]) / denom
		dic[key] = dictionary[key]

	sorted_d = dict( sorted(dic.items(), key=operator.itemgetter(1),reverse=True))
	return sorted_d

#Load words
file_name = input('enter file name: ')
threadLock = threading.Lock()
File = open(file_name, 'r')
bag_of_word = File.readlines()
File.close()
for i in range(len(bag_of_word)):
	bag_of_word[i] = bag_of_word[i][:-1]

#extract possible labels
possible_labels = []
for word in bag_of_word:
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
		cnt = 0;
		for word in bag_of_word:
			if word in label_description:
				cnt += 1
		thread_explored_data.append( [self.label, cnt])
				
cnt = 0

threads  = []

for possible_label in possible_labels:
	try:
		new_thread = data_extraction_thread(possible_label)
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

print(soft_and_sort(label_score))

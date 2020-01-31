from TopicLabeling import TopicLabeling
import warnings

warnings.simplefilter("ignore")

file_name = 'top_words.csv'
File = open(file_name, 'r')
All_file = File.readlines()
File.close()

All_file = All_file[1:]
labels = {}
for line in All_file:
	L = line.split('\t')
	if L[1] not in labels.keys():
		labels[L[1]] = []
	labels[L[1]].append(L[2])

assigned = {}

File = open('assigned labels','w', encoding="utf-8")

cnt = 0
for k in labels.keys():
	persian_words = labels[k]
	topic_labeling = TopicLabeling(persian_words)
	assigned[k] = topic_labeling.assign_label()
	File.write(str(k) + ',' + str(assigned[k]) + '\n')
	cnt += 1
	if cnt == 2:
		break

File.close()
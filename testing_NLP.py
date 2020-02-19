from TopicLabeling import TopicLabeling
import warnings

warnings.simplefilter("ignore")

file_name = './assets/word_list_farsi_test_1'
File = open(file_name, 'r', encoding = "utf-8")
All_file = File.readlines()
File.close()

for i in range(0,len(All_file)):
	All_file[i] = All_file[i][:-1]

topic_labeling = TopicLabeling(All_file)
print(topic_labeling.assign_label())

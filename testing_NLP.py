from TopicLabeling import TopicLabeling
import warnings

warnings.simplefilter("ignore")

print('enter file address: ')
file_name = input()
File = open(file_name, 'r')
persian_words = File.readlines()
File.close()

topic_labeling = TopicLabeling(persian_words)
print(topic_labeling.assign_label())
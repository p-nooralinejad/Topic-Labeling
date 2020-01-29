# Topic-Labeling
This is my B.Sc. Thesis project. In this project, I have to take input a text, essay, paper, thesis, dissertation, etc, and assign a label based on the content. In other words, it will take a text as an input and outputs that what is the text about. The challenge is that it had to be bilingual (e.g. persian and english) and it had to be as specific as possible.

Using the LDA algorithm, we extract keywords of the text and then, with the code of this repository and thanks to huge dataset of wikipedia, we find a page in wikipedia which is the most likely page to this bag of words and we use it's title as our label to the text topic.

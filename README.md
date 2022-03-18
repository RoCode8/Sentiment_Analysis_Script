# Sentiment Analysis on Web Scraped Data

Introduction- The objective of this project was to perform text analysis to derive
sentimental opinion, sentiment scores, readability analysis. The text is being extracted
from the list url file in .csv or .xlsx .

## Thought Process:-

● The data from Input.xlsx file is extracted and saved in a dataframe. This will help to
iterate through each row and will get access to each url provided in the file one by
one.
● Each url is accessed and acts as a source for text to which sentimental analysis is
done.
● The Beautiful soup library from python helps in pulling text from the website using
the urls as input.
● The data pulled from the website is pasted in text format to a new text file.
● The text file is accessed for cleaning and stop word removal and the text is stored
in string variable, declaring this variable provides easy access to each text on
every iteration and then lemmatization can be done.
● Lemmatization is the process of grouping together the inflected word from
stopword removal and cleaning process. It helps in adding context to words that
can be used in textual analysis.
● Then the lemmatized words are stored in a data frame, this helps in getting the
count of the number of words extracted from cleaning and lemmatization.
● After changing the case of each word in the data frame it is converted to a list so
that further calculation can be performed.

## Text Analysis Variable Definition:-

Positive Score: This score is calculated by assigning the value of +1 for each word if
found in the Positive Dictionary and then adding up all the values.
Negative Score: This score is calculated by assigning the value of -1 for each word if
found in the Negative Dictionary and then adding up all the values. We multiply the score
with -1 so that the score is a positive number.
Polarity Score: This is the score that determines if a given text is positive or negative in
nature. It is calculated by using the formula:
Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) +
0.000001)
Range is from -1 to +1
Subjectivity Score: This is the score that determines if a given text is objective or
subjective. It is calculated by using the formula:
Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) +
0.000001)
Range is from 0 to +1
Average Sentence Length = the number of words / the number of sentences
Percentage of Complex words = the number of complex words / the number of words
Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
Average Number of Words Per Sentence = the total number of words / the total number
of sentences.

## Variable Used:-

* url_ID=stores url serial number
* urls=stores the urls extracted from excel file
* t_word_count=stores total number of words from text
* t_char_count=stores total number of character from text
* complex_word_count=stores total number of complex word count from text
* syllable_count=stores syllable_count
* wordcount= stopwords from nltk and punctuation removed
* pscore=stores positive score
* nscore=stores negative score
* polarity_score=stores polarity score
* subjectivity_score=stores subjectivity score
* number_of_sentences=stores number of sentence in the extracted text
* avg_sentence_length=stores the average sentence length
* percentage_of_complex_words=stores the percent of complex words
* avg_no_of_words_per_sentence=stores the avg number of words per sentence
* fog_index=stores fog index
* personal_pronouns=stores personal pronouns
* avg_word_length=stores avg word length

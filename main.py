import requests
import nltk
from bs4 import BeautifulSoup
import pandas as pd 
import re
# tokenization
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
# POS tagging
from nltk import pos_tag
# to map pos tags to wordnet tags
from nltk.corpus import wordnet
# stopwords
#nltk.download('stopwords')
from nltk.corpus import stopwords
# Lemmatization
from nltk.stem import WordNetLemmatizer
#Text Statistics: return a dictionary with wordcount , number of  syllables etc
from textatistic import Textatistic

#declared variables -- type-list
url_ID=[] #stores url serial number
urls=[] #stores the urls extracted from excel file
t_word_count=[] #stores total number of words from text
t_char_count=[] #stores total number of character from text
complex_word_count=[] #stores total number of complex word count from text
syllable_count=[] #stores syllable_count
wordcount=[] # stopwords from nltk and punctuation removed 
pscore=[] #stores positive score
nscore=[] #stores negative score
polarity_score=[] #stores polarity score
subjectivity_score=[] #stores subjectivity score
number_of_sentences=[] #stores number of sentence in the extracted text
avg_sentence_length=[] #stores the avg sentence lenght
percentage_of_complex_words=[] #stores the percent of complex words
avg_no_of_words_per_sentence=[] #stores the avg number of words per sentence
fog_index=[] #stores fog index 
personal_pronouns=[] #stores personal pronouns
avg_word_length=[] #stores avg word length

#Reading .xlsx file to extract urls
df = pd.read_excel(r"C:\Users\RR\Desktop\DE INTERN ASSIGNMENT\code\Input.xlsx")

#Declaring Dictionary of positve and negative words
def IsNotNull(value):
	    return value is not None and len(value) > 0
dict_p = []
f = open('positive - master dictionary.txt', 'r')
for line in f:
    t = line.strip().lower()
    if IsNotNull(t):
            dict_p.append(t)
f.close

dict_n = []
f = open('negative - master dictionary.txt', 'r')
for line in f:
    t = line.strip().lower()
    if IsNotNull(t):
	    dict_n.append(t)
f.close


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
for i in range(0,170): # 170 is the total number rows in the dataframe containing urls
    #Extracting URL from .csv file for web scrapping
    a=df['URL'][i]
    html=requests.get(a,headers=headers).text
    soup=BeautifulSoup(html,"html.parser")
    title=soup.find_all('h1',{'class':'entry-title'})
    all_links=soup.find_all('div',{'class':'td-post-content'})
    str_cell= str(title+all_links)
    #Pasting all the scape text in url_text variable
    url_text = BeautifulSoup(str_cell, "html.parser").get_text()
    with open(f"{i+1}.txt",'w', encoding="utf-8") as f:f.write(url_text) #saving the scape data in file
    with open(f"{i+1}.txt", 'r', encoding="utf-8") as file:
      cleartext = file.read().rstrip()
    
    urls.append(a)
    url_ID.append(i+1)

    #Cleaning of text by removing extra spaces , special characters etc
    clean_text= cleartext.replace("n", " ")
    clean_text= cleartext.replace("/", " ")      
    clean_text= ''.join([c for c in clean_text if c != "'"])
    clean_text = re.sub('[^A-Za-z]+', ' ', clean_text) 

    #Funtion which return Syllable Count
    def sybl_c(str):   
        s = Textatistic(cleartext)
        s.counts
        return syllable_count.append(s.counts['sybl_count'])
    sybl_c(cleartext)

    #Calculating total number of words in the cleaned text
    t_word_count.append(len(clean_text.split()))

    #Calculating number of personal pronouns - 'I','we','my','ours','us'
    personal_pronouns.append(len(re.findall('I|we|We|my|My|Our|Ours|ours|our|Us|us', cleartext)))

    #returns number of sentences in the extracted text
    number_of_sentences.append(len(sent_tokenize(cleartext,'english')))

    #Funtion which returns complex word count-it is number of words which contains more than 2 syllable
    def complex_count(str):
        comp_count=0
        count=0
        syllables = set("AEIOUaeiou")
    
        for letter in str:
            if letter in syllables:
                count = count + 1
                if count>=2:
                    comp_count +=1
      
        complex_word_count.append(comp_count)
    complex_count(clean_text)

    # Lemmatization
    # POS tagger dictionary
    pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
    #Instantiate WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    lemma = []
    pos = pos_tag(word_tokenize(clean_text))
    for ele, tag in pos:
        tag = pos_dict.get(tag[0])
        if ele.lower() not in stopwords.words('english'):
            if not tag:
                lemma.append(ele)
            else:
                lemma.append(wordnet_lemmatizer.lemmatize(ele, tag))
            
    #Converting all words to lowercase
    for i in range(len(lemma)):
        lemma[i]=lemma[i].lower()

    #Creating a dataframe 
    df1= pd.DataFrame(lemma,columns=['Words'])         
    wl=df1['Words'].tolist()
    #returns the total number of words in the data frame
    wordcount.append(len(wl))

    #return the total number character in the list of words
    ch=0
    for i in range(0,len(wl)):
        ch=len(wl[i])+ch
    t_char_count.append(ch)

    #return Possitive and Negative scores of a text
    p=0
    n=0
    for e in dict_p :
        if e in wl:p+=1
    pscore.append(p)
    for e1 in dict_n:
        if e1 in wl:n+=1
    nscore.append(n)

# Calculation of Text Analysis Parameters

for i in range(0,len(pscore)):
    polarity_score.append((pscore[i]-nscore[i])/((pscore[i]+nscore[i])+0.000001))

for i in range(0,len(pscore)):
    subjectivity_score.append((pscore[i]+nscore[i])/((wordcount[i])+0.000001))

for i in range(0,len(t_word_count)):
    avg_sentence_length.append(t_word_count[i]/number_of_sentences[i])

for i in range(0,len(complex_word_count)):
    percentage_of_complex_words.append((complex_word_count[i]/t_word_count[i]))

for i in range(0,len(t_word_count)):
    avg_no_of_words_per_sentence.append(t_word_count[i]/number_of_sentences[i])

for i in range(0,len(avg_sentence_length)):
    fog_index.append(0.4*(avg_sentence_length[i]+percentage_of_complex_words[i]))

for i in range(0,len(t_char_count)):
    avg_word_length.append(t_char_count[i]/wordcount[i])

details={'URL_ID':url_ID
     ,'URL':urls
     ,'POSITIVE SCORE':pscore
     ,'NEGATIVE SCORE':nscore
     ,'POLARITY SCORE':polarity_score
     ,'SUBJECTIVITY SCORE':subjectivity_score
     ,'AVG SENTENCE LENGTH':avg_sentence_length
     ,'PERCENTAGE OF COMPLEX WORDS':percentage_of_complex_words
     ,'FOG INDEX':fog_index
     ,'AVG NUMBER OF WORDS PER SENTENCE':avg_no_of_words_per_sentence
     ,'COMPLEX WORD COUNT':complex_word_count
     ,'WORDCOUNT':wordcount
     ,'SYLLABLE PER WORD':syllable_count
     ,'PERSONAL PRONOUNS':personal_pronouns
     ,'AVG WORD LENGTH':avg_word_length}

# Creating a dataframe and saving the dictionary data
df2=pd.DataFrame.from_dict(details)

#saving the data frame to excel sheet
filename='text.xlsx'
df2.to_excel(filename,index=False)
print('file created!!')
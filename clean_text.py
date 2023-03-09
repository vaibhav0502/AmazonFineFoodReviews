import re
import string
from itertools import groupby
from bs4 import BeautifulSoup
import contractions

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem.wordnet import WordNetLemmatizer

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


STOPWORDS =  [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',  "it's", 'its', 
    'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',  'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',  'or', 'because', 'as', 'until', 'while', 'of', 'at',  'for', 'with',
    'about', 'between', 'into',  'through', 'during',  'to',  'from', 
    'in', 'out', 'on', 'off',  'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',  'other', 'some', 'such', 'only', 'own', 
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',  "didn't", 'doesn', 
    "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', 
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 
    'won', "won't", 'wouldn', "wouldn't", "would", "could"
]

class TextProcess:

  def __init__(self, df=None, stopwords=STOPWORDS):
    self.df = df
    self.stopwords = stopwords

  def decontracted(self, text):
      '''
      Function to expand the shotened words: what've ---> what have
      '''
      expanded_words = []    
      for word in text.split():
        # using contractions.fix to expand the shotened words
        expanded_words.append(contractions.fix(word))   

      expanded_text = ' '.join(expanded_words)
      return expanded_text

  def remove_stopwords(self, text):
      text = text.strip().split()
      text = [word for word in text if word not in self.stopwords and len(word)>1]
      return ' '.join(text)

  def remove_html_tags(self, text):
      '''Remove html tags'''
      return BeautifulSoup(text, 'lxml').get_text()

  def remove_consecutive_duplicate(self, text):
      '''Remove consecutive duplicate'''
      text = text.split()
      text = [i[0] for i in groupby(text)]
      return " ".join(text)

  def remove_space(self, text):
      # text = re.sub('[^\w\s]', ' ', text)   # remove punc
      text = re.sub("[\s]+", ' ', text)
      return text

  def remove_punc(self, text):
      # text = re.sub('[^\w\s]', ' ', text)   # remove punc
      text = [word for word in text.split() if word not in string.punctuation]
      text = " ".join(text)
      text = re.sub("[\s]+", ' ', text)
      return text

  def nltk_tag_to_wordnet_tag(self, nltk_tag):
      if nltk_tag.startswith('J'):
          return wordnet.ADJ
      elif nltk_tag.startswith('V'):
          return wordnet.VERB
      elif nltk_tag.startswith('N'):
          return wordnet.NOUN
      elif nltk_tag.startswith('R'):
          return wordnet.ADV
      else:
          return None

  def lemmatize_sentence(self, sentence):
      lemmatizer = WordNetLemmatizer() 
      #tokenize the sentence and find the POS tag for each token
      nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))

      #tuple of (token, wordnet_tag)
      wordnet_tagged = map(lambda x: (x[0], self.nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)

      lemmatized_sentence = []
      for word, tag in wordnet_tagged:
          if tag is None:
              #if there is no available tag, append the token as is
              lemmatized_sentence.append(word)
          else:
              #else use the tag to lemmatize the token
              lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))

      return self.remove_stopwords(" ".join(lemmatized_sentence))

  def token(self, text):
    text = nltk.word_tokenize(text)
    return " ".join(text)

  def clean_text(self, sentence):
    '''
    Function to clean the text and remove all the unnecessary elements.
    '''
    sentence = sentence.lower()                     # make the text lowercase
    sentence = self.token(sentence)
    sentence = self.decontracted(sentence)          # expand the shotened words   what've ---> what have
    # sentence = self.remove_html_tags(sentence)
    sentence = self.remove_punc(sentence)
    sentence = self.remove_space(sentence)
    sentence = self.remove_consecutive_duplicate(sentence)
    sentence = re.sub('[^A-Za-z]+', ' ', sentence)
    sentence = self.remove_stopwords(sentence)
    sentence = self.lemmatize_sentence(sentence)
    return sentence

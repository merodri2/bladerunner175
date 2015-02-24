#nltk imports
import nltk
from nltk.util import ngrams
from nltk import PorterStemmer as PorterStemmer
from nltk import Text
from nltk import FreqDist
from nltk.corpus import stopwords as _stopwords

#SK-learn imports
from sklearn.feature_extraction.text import CountVectorizer

#collection and other imports
from collections import Counter
from re import search as regexpSearch
from string import punctuation as punctuationList
from random import randint as randomInteger

# Utilities module:

#constants
stopwords = _stopwords.words('english')
stopwords.extend(["i'm","it's",'im','its']) #these tokens are common to both positive and negative

def word_tokenize(toTokenize):
    #Split by space
    _tokens = toTokenize.lower().split(' ')
    #Strip punctuation (leading and trailing)
    return [token.strip(punctuationList) for token in _tokens]


def bigrams(toTokenize):
        tokens = word_tokenize(toTokenize)
        bi_grams = list(ngrams(tokens,2))
        return bi_grams
        
def trigrams(toTokenize):
        tokens = word_tokenize(toTokenize)
        tri_grams = list (ngrams(tokens,3))
        return tri_grams

def uppercase_count(tweet): 
    upCount = 0
    tweet_tokens = nltk.word_tokenize(tweet)    
    for token in tweet_tokens:
        if token.isupper():
            upCount += 1
    return upCount

def negation_count(tweet):
    negCount = 0
    tweet_tokens = word_tokenize(tweet)
    for token in tweet_tokens:
        if token in negation_words:
            negCount += 1
    return negCount
        
def hashtag_count(tweet):
    hashtagCount = 0
    tweet_tokens = nltk.word_tokenize(tweet)
    for token in tweet_tokens:
        if token == '#':
            hashtagCount+= 1           
    return hashtagCount
 
def tweet_pos_tags(tweet_tokens):
    return nltk.pos_tag(tweet_tokens)

def count_pos_tags(pos_list, normalized = 0):    
    pos_counts = Counter(tag for word,tag in pos_list)
    total = sum(pos_counts.values())
    if normalized == 1:
        final_counts = dict((word,float(count)/total) for word,count in pos_counts.items())
    else:
        final_counts = dict(pos_counts)
    return final_counts
  
# Dynamic Stopword list generated by terms that only appear once
def tf1_SWGenerator(tweetCollection, ngram = 1):
    count_vect = CountVectorizer(tweetCollection, ngram_range = (ngram,ngram), max_df = 1)
    count_vect.fit(tweetCollection)
    tf1_list = count_vect.get_feature_names()
    return tf1_list 
    
# Dynamic Stopword list generated by terms that appear very often
def tfh_SWGenerator(tweetCollection, ngram = 1,feat_count = 500):
    count_vect = CountVectorizer(tweetCollection,ngram_range = (ngram,ngram), max_features = feat_count)
    count_vect.fit(tweetCollection)    
    tfh_list = count_vect.get_feature_names()
    return tfh_list

    
def word_stemmer(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def exclude_stopwords(tokens):
    return [token for token in tokens if token not in stopwords]

def remove_punctuation(tokens):
    #remove token that has only punctuations
    #different than strip from word_tokenize()
    return [token for token in tokens if regexpSearch(r'\w',token)]

def preprocess_tweet_noStem(tweetString):
    '''
    :param tweetString: String
    :return: preprocessed token
    Processing Rule:
    - Split tweetString into tokens
    - Exclude Stopwords
    - Remove Punctuation
    '''
    #tokenize (nltk default tokenizer, Treebank tokenizer)
    _tokens = word_tokenize(tweetString)
    _tokens = exclude_stopwords(_tokens)
    _tokens = remove_punctuation(_tokens)
    return _tokens


def preprocess_tweet_stem(tweetString):
    '''
    :param tweetString: String
    :return: preprocessed token
    Processing Rule:
    - Split tweetString into tokens
    - Exclude Stopwords
    - Remove Punctuation
    - Normalize token using PorterStemmer Algorithm from nltk
    '''
    _tokens = word_tokenize(tweetString)
    _tokens = exclude_stopwords(_tokens)
    _tokens = remove_punctuation(_tokens)
    _tokens = word_stemmer(_tokens)
    return _tokens

def _obtain_index(count,both=0):
    random_index = []
    if both == 1:
        while len(random_index) < count/2:
            randint = randomInteger(0,800000)
            if randint not in random_index:
                random_index.append(randint)
        while len(random_index) < count:
            randint = randomInteger(800001,1600000)
            if randint not in random_index:
                random_index.append(randint)
    else:
        while len(random_index) < count:
            randint = randomInteger(0,800000)
            if randint not in random_index:
                random_index.append(randint)

    return sorted(random_index)

def generate_text_object(tokens, stopword=0):
    _tokens = []
    if stopword == 1:
        for tweet in tokens:
            _tokens.extend(tweet.get_tweet_tokens())
    else:
        for tweet in tokens:
            _tokens.extend(tweet.get_tweet_tokens())
    return Text(_tokens)

def get_frequency_distribution(text):
    return FreqDist(text)
#Sentiment Dictionary originally based on positive and neg 
#from http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
    
def build_Sentiment_Dictionary(pos_file,neg_file):
    
    sent_dict = {}
    
    pos_f = open(pos_file)
    neg_f = open(neg_file)
    
    for line in pos_f:
        sent_dict[line.strip()] = "positive"
    
    for line in neg_f:
        sent_dict[line.strip()] = "negative"
        
    return sent_dict
        
def uni_LS_Score(tweet, sent_dict):
    lexscore = 0       
    
    tweet_tokens = word_tokenize(tweet)    
    
    for token in tweet_tokens:
        if token in sent_dict:
            if sent_dict[token] == "positive":
                lexscore += 1
            elif sent_dict[token] == "negative":
                lexscore -= 1
     
    return lexscore

def lex_label(s_lexscore):
    if s_lexscore < 0:
        return "Negative"
    elif s_lexscore > 0:
        return "Positive"
    else:
        return "Neutral"


























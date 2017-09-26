# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:49:09 2017

@author: nahid
"""

#import regex
import re
import csv 
import os
import nltk
     #Read the tweets one by one and process it
inpTweets = csv.reader(open('Airline.csv',"rt",encoding="Latin-1"), delimiter=',', quotechar='|')

def processTweet2(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet   

#end loop
#start extract_features
###get stopword list
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

stopWords = []

st = open('stopwords.txt', 'r')
stopWords = getStopWordList('stopwords.txt')


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

import nltk
training_set = nltk.classify.util.apply_features(extract_features, tweets)
# Train the classifier Naive Bayes Classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
#ua is a dataframe containing all the united airline tweets
ua['sentiment'] = ua['tweets'].apply(lambda tweet: NBClassifier.classify(extract_features(getFeatureVector(processTweet2(tweet)))))


from __future__ import division
import parse #This is our parser program which returns a sentence from the file
import re
import nltk
from nltk.corpus import stopwords
import random
from urllib import urlopen
import os
import string

def cheap_classifier(training_data):
    dictionary={}
    for sentence, score in training_data.items():
        sentence = nltk.word_tokenize(sentence)
        sentence = [w.rstrip(string.punctuation).lstrip(string.punctuation) for w in sentence]
        for word in sentence:
            if word in stopwords.words('english'):
                dictionary[word] = (0, 1)
            else:
                try:
                    total_score, count = dictionary[word]
                    total_score+=score
                    count+=1
                    dictionary[word] = (total_score, count)      
                except:
                    dictionary[word]= (score, 1)
                
    dictionary_of_average_score = {}
    for key in dictionary.keys():
        tot_score, tot_count = dictionary[key]
        dictionary_of_average_score[key] = tot_score/tot_count
    return dictionary_of_average_score

# -*- coding: utf-8 -*-
from __future__ import division
import nltk, string, math, csv, parse, os, random, re, numpy
wnl = nltk.WordNetLemmatizer()

import h_features
import n_feature
import sFeature
import tristan_features


posfile = open('wordstat/positive.csv', 'rb')
negfile = open('wordstat/negative.csv', 'rb')
litfile = open('wordstat/litigious.csv', 'rb')
unfile = open('wordstat/uncertainty.csv', 'rb')
weakfile = open('wordstat/modalWeak.csv', 'rb')
strongfile = open('wordstat/modalStrong.csv', 'rb')
reader1 = csv.reader(posfile)
reader2 = csv.reader(negfile)
reader3 = csv.reader(litfile)
reader4 = csv.reader(unfile)
reader5 = csv.reader(weakfile)
reader6 = csv.reader(strongfile)
pos = set() 
for row in reader1:
    if len(row) == 1:
        pos.add(row[0].lower())
neg =  set()
for row in reader2:
    if len(row) == 1:
        neg.add(row[0].lower())
lit = set()
for row in reader3:
    if len(row) == 1:
        lit.add(row[0].lower())
un = set() 
for row in reader4:
    if len(row) == 1:
        un.add(row[0].lower())
weak = set()
for row in reader5:
    if len(row) == 1:
        weak.add(row[0].lower())
strong = set()
for row in reader6:
    if len(row) == 1:
        strong.add(row[0].lower())


def get_features(sent):
	z= h_features.get_function_features(sent)
	z.update(n_feature.n_structural_features(sent))
	z.update(sFeature.sFeature(sent))
	z.update(tristan_features.syntactic_features(sent))
	z.update(tristan_features.char_based_features(sent))


train_base_path = "data/training/"
train_files = ["Canon PowerShot SD500.txt", "Canon S100.txt", "Diaper Champ.txt", "Hitachi router.txt", "ipod.txt", "Linksys Router.txt", "MicroMP3.txt","Nokia 6600.txt", "norton.txt"]

training_data = {}
for train_file in train_files:
    train_path = os.path.join(train_base_path, train_file)
    parse.read_txt_data(train_path, training_data)


held_base_path = "data/heldout/"
held_files = ["Apex AD2600 Progressive-scan DVD player.txt", "Canon G3.txt", "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt", "Nikon coolpix 4300.txt", "Nokia 6610.txt"]

held_data = {}
for held_file in held_files:
    held_path = os.path.join(held_base_path, held_file)
    parse.read_txt_data(held_path, held_data)


training_data = parse.val_to_polarity(training_data)
held_data = parse.val_to_polarity(held_data)

 
#testing
feature_sets = [(get_features(n), v) for (n,v) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets) * 0.9)
print "trainging results"
train_set, test_set = feature_sets[size:], feature_sets[:size] ####confused as to why we need two test sets????????? 
#train_set = [line for line in train_set if line]


classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

print " heldout results"
train_set = feature_sets
test_set = [(get_features(n), v) for (n,v) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()



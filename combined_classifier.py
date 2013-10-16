# -*- coding: utf-8 -*-
from __future__ import division
import nltk, string, math, csv, os, random, re, numpy
wnl = nltk.WordNetLemmatizer()

import h_features
import n_feature
import sFeature
import tristan_features
import parse

def get_features(sent):
    #z = h_features.get_function_features(sent)
    #z.update(n_feature.n_structural_features(sent))
    #z.update(sFeature.sFeature(sent))
    #z.update(tristan_features.syntactic_features(sent))
    z = tristan_features.char_based_features(sent)
    return z

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

#classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier = nltk.DecisionTreeClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
#classifier.show_most_informative_features()

print " heldout results"
train_set = feature_sets
test_set = [(get_features(n), v) for (n,v) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
#classifier.show_most_informative_features()

final_test_files = ['product1.txt', 'product2.txt', 'product3.txt',
                     'product3.txt']
final_test_path = "sampleOutput/"
output_file_path = "sampleOutput/classified_output.txt"
output = f = open(output_file_path, 'w+')

test_file_dict = {} #dict of dicts
for final_test_file in final_test_files:
    parse.val_to_polarity(held_data)
    file_dict = parse.read_test_data(os.path.join(final_test_path, final_test_file))
    test_file_dict[final_test_file] = file_dict

print test_file_dict #dict of dict. {"product1.txt":{"sent":1...}, "product2":}

for file_name, text_dict in test_file_dict.items():
    for line_num, sentence in text_dict.items():
        #print "DO file: %s, %s, %s" % (file_name, line_num, sentence)
        #print "%s\t%s\t%s" % (file_name, line_num, classifier.classify(get_features(sentence)))
        output.write("%s\t%s\t%s\n" % (file_name, line_num, classifier.classify(get_features(sentence))))

output.close()





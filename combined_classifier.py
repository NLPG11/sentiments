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
    #print sent
    #z.update(hn_feature.n_structural_features(sent))
    z = n_feature.n_structural_features(sent)
    #z = tristan_features.char_based_features(sent)
    #z.update(tristan_features.char_based_features(sent))
    #z.update(tristan_features.syntactic_features(sent))
    #z.update(n_feature.n_structural_features(sent))
    #z.update(sFeature.sFeature(sent))
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
print "training results"
train_set, test_set = feature_sets[size:], feature_sets[:size]

#print train_set
classifier = nltk.NaiveBayesClassifier.train(train_set)
#classifier = nltk.DecisionTreeClassifier.train(train_set)
#classifier = nltk.MaxentClassifier.train(train_set)
#classifier = nltk.weka.WekaClassifier.train(train_set)

#polarized_held_data
#polatized_test_set = [(get_features(n), v) for (n,v) in polarized_held_data.items()]
held_test_set = [(get_features(n), v) for (n,v) in held_data.items()]

a = []
b = []
print len(held_test_set)
for t in held_test_set:
    #pass
    #print t[1]
    #print classifier.classify(t[0])
    a.append(t[1])
    b.append(classifier.classify(t[0]))

correct = 0.0
incorrect = 0.0
#print classified_result
for i in xrange(0, len(b)):
    if parse.rangefy(a[i]) == parse.rangefy(b[i]):
        correct+=1
    else:
        incorrect+=1
perc = correct/(correct+incorrect)
print correct
print incorrect
print "TRUE VALUE: %s" % perc


print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

print " heldout results"
train_set = feature_sets
test_set = [(get_features(n), v) for (n,v) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

final_test_files = ['product1.txt', 'product2.txt', 'product3.txt']
final_test_path = "data/testdata/"
output_file_path = "data/testdata/classified_output.txt"
output = f = open(output_file_path, 'w+')

test_file_dict = {} #dict of dicts
for final_test_file in final_test_files:
    file_dict = parse.read_test_data(os.path.join(final_test_path, final_test_file))
    test_file_dict[final_test_file] = file_dict

print len(test_file_dict) #dict of dict. {"product1.txt":{"sent":1...}, "product2":}

for file_name in final_test_files:
    text_dict = test_file_dict[file_name]
    keys = [int(k) for k in text_dict.keys()]
    keys.sort()
    print keys
    for key in keys:
        line_num = key
        sentence = text_dict[str(key)]
        if "[t]" not in sentence:
            output.write("%s\t%s\t%s\n" % (file_name, line_num, classifier.classify(get_features(sentence))))
        else:
            output.write("%s\t%s\t%s\n" % (file_name, line_num, 0))

output.close()


a = "This is the worst product ever"
print a
print classifier.classify(get_features(a))

a = "This is the worst product ever. I will never buy this piece of shit. terrible. terrible terrible! I mean, I can't believe how bad it is!. blah!"
print a
print classifier.classify(get_features(a))


a = "This is pretty damn awesome. I would definitely buy again"
print a
print classifier.classify(get_features(a))

a = "It is better than the competition, by far!"
print a
print classifier.classify(get_features(a))


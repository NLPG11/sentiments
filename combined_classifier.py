import nltk, numpy
import parse
import re
import random
import nltk

import h_features
import n_feature
import sFeature
import tristan_features


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
feature_sets = [(get_function_features(n), v) for (n,v) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets) * 0.9)
print "trainging results"
train_set, test_set = feature_sets[size:], feature_sets[:size]
#train_set = [line for line in train_set if line]


classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

print " heldout results"
train_set = feature_sets
test_set = [(get_function_features(n), v) for (n,v) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()



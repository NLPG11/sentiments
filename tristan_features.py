import parse
import re
import random
import nltk
import os

##################################TRAIN DATA ACUISITION########
train_base_path = "data/training/"
train_files = ["Canon PowerShot SD500.txt", "Canon S100.txt", "Diaper Champ.txt",
               "Hitachi router.txt", "ipod.txt", "Linksys Router.txt", "MicroMP3.txt",
              "Nokia 6600.txt", "norton.txt"]

training_data = {}

for train_file in train_files:
    train_path = os.path.join(train_base_path, train_file)
    parse.read_txt_data(train_path, training_data)

##################################HELD DATA ACUISITION########
held_base_path = "data/heldout/"
held_files = ["Apex AD2600 Progressive-scan DVD player.txt", "Canon G3.txt", "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt",
               "Nikon coolpix 4300.txt", "Nokia 6610.txt"]
held_data = {}






def char_based_features(sent):
    '''
    F1 total number of characters in words(C)
    F2 total number of letters(a-z)/C
    F3 total number of upper characters/C
    F4 total number of digital characters/C
    F5 total number of white-space characters/C
    F6 total number of tab space characters/C
    F7 : : : F29 number of special characters(%,etc.)/C(23 features)
    '''
    ret = {}
    #ret["t_sent_length"] = len(sent)
    ret["t_alpha_length"] = len([c for c in sent if c.isalpha()])
    ret["t_upper_length"] = len([c for c in sent if c.isupper()])
    ret["t_digit_length"] = len([c for c in sent if c.isdigit()])
    ret["t_space_length"] = len([c for c in sent if c == ' '])
    ret["t_tab_length"] = len([c for c in sent if c == '\t'])
    ret["t_special_length"] = len(re.findall("\W", sent)) - ret["t_space_length"]
    return ret

#char_based_features("The ipod sucks!&@") #testing

training_data = parse.val_to_polarity(training_data)
feature_sets = [(char_based_features(n), g) for (n,g) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets) * 0.9)
train_set, test_set = feature_sets[size:], feature_sets[:size]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)

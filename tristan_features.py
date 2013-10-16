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
for held_file in held_files:
    held_path = os.path.join(held_base_path, held_file)
    parse.read_txt_data(held_path, held_data)

training_data = parse.val_to_polarity(training_data)
held_data = parse.val_to_polarity(held_data)

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
    ret["t_sent_length"] = len(sent) > 100
    ret["t_alpha_length"] = len([c for c in sent if c.isalpha()]) > 0
    ret["t_upper_length"] = len([c for c in sent if c.isupper()]) > 0
    ret["t_digit_length"] = len([c for c in sent if c.isdigit()]) > 0
    #ret["t_space_length"] = len([c for c in sent if c == ' '])
    ret["t_tab_length"] = len([c for c in sent if c == '\t'])
    #ret["t_special_length"] = (len(re.findall("\W", sent)) - ret["t_space_length"])
    return ret

#char_based_features("The ipod sucks!&@") #testing
feature_sets = [(char_based_features(n), g) for (n,g) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets) * 0.9)
print "CHAR BASED FEATURE RESULTS SELF TEST"
train_set, test_set = feature_sets[size:], feature_sets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

print "CHAR BASED FEATURE RESULTS HELDOUT DATA TEST"
traiin_set = feature_sets
test_set = [(char_based_features(n), g) for (n,g) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

def syntactic_features(sent):
    '''
    #F131 number of single quotes(')/C
    F133 number of periods(.)/C
    F134 number of colons(:)/C
    F135 number of semi-colons(;)/C
    F136 number of question marks(?)/C
    *F137 number of multiple question marks(???)/C
    F138 number of exclamation marks(!)/C
    *F139 number of multiple exclamation marks(!!!!)/C
    F140 number of ellipsis(. . . ) /C
    '''
    ret = {}
    ret["t_s_quotes_length"] = len([c for c in sent if c == "\'"])
    ret["t_s_comma_length"] = len([c for c in sent if c == ","])
    ret["t_s_period_length"] = len([c for c in sent if c == "."])
    ret["t_s_colon_length"] = len([c for c in sent if c == ":"])
    #ret["t_s_sem_colon_length"] = len([c for c in sent if c == ";"])
    ret["t_s_question_length"] = len([c for c in sent if c == "?"])
    #ret["t_s_exclam_length"] = len([c for c in sent if c == "!"])
    #ret["t_s_ellip_length"] = len([c for c in sent if c == "..."])
    return ret


print "SYNTACTIC FEATURE RESULTS"
feature_sets = [(syntactic_features(n), g) for (n,g) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets) * 0.9)
train_set, test_set = feature_sets[size:], feature_sets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()

print "CHAR BASED FEATURE RESULTS HELDOUT DATA TEST"
traiin_set = feature_sets
test_set =  [(char_based_features(n), g) for (n,g) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()


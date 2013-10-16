from __future__ import division
import parse #This is our parser program which returns a sentence from the file
import re
import nltk
from nltk.corpus import stopwords
from shutil import move
from os import remove, close
import random
from urllib import urlopen
import os
import string
import ngoc_features
#import ngoc_features
def parse_data_set(training_path):
    training_files = []
    for subdir, dirs, files in os.walk(training_path):
        for a_file in files:
            if '.txt' in a_file:
                training_files.append(a_file)
    training_data ={}
    for a_file in training_files:
        new_training_path = os.path.join(training_path, a_file)
        parse.read_txt_data(new_training_path, training_data)
    return training_data



training_data = parse_data_set("data/training/")
held_data = parse_data_set("data/heldout/")

#Turn all Results to -1 to 1
training_data = parse.val_to_polarity(training_data)
held_data = parse.val_to_polarity(held_data)

'''This is a structural feature that does the following:
    F145 average number of chars per word
F147 average number of words per sentence


F148 number of words beginning with upper case/S
F149 number of words beginning with lower case/S


F148 number of words that are all caps 
F152 absence/present of profanity
F153 absence/present of positive words
(as you define, but maybe like, love, etc. )
'''
profanity_words = ''' abandon, boot, cynical, drab, guilt, killer,
                    perplex, selfishness, thud, yearn, yelp,
                    accident, alarming, apathy, backwardness,
                    betray, broke, catch, collide, confrontation,
                    covet, deafness, demean, deter, disavowal,
                    disproportionate, dungeon, evasion, fallout,
                    flagrant, frown, harmful, hot,
                    impetuous, inefficiency, interrupt, liar,
                    manipulate, misuse, neutralize, ordeal,
                    plod, punch, recoil, revert, sadness,
                    shark, slanderous, spite, strife, suspend,
                    trap, undignified, unqualified, vanity, weariness,
                    affliction, anguish, atrophy, bastard,
                    blindness, butchery, circle, complicate,
                    contradiction, criticize, defect, deride,
                    difficulty, dishearten, disturb, enrage,
                    expense, feign, forlorn, gloat, hell,
                    ignorant, incompetence, injunction, irrational,
                    loveless, misbehavior, murder, obsolete,
                    overwhelming, presumptuous, rampant,
                    reprehensible, rotten, scorn, shroud,
                    smuggle, static, substitution, tempest, ugly,
                    unguarded, untrustworthy, volatile, woe'''
positive_words = '''able, convince, famous, imperative,
                   negotiate, real, sturdy, wonder, zest, accommodate, adjust,
                   affirmation, amiable, arisen, ball, blithe, careful,
                   cleanliness, commendation, consistent, cure, desirable,
                   earnestness, entertain, exuberance, flexible, gaiety,
                   good, harmonious, humble, innovative, joke, luckily,
                   meaningful, momentous, optimal, peaceful, precaution,
                   profit, purposeful, religious, richness, satisfy,
                   sincere, stately, sweet, treaty, upright, vitality,
                   witty, woo, workmanship, worth, worth-while, zenith,
                   acquit, advance, alleviate, applause, augment, beneficent,
                   brilliance, cheerful, collaborate, comprehensive, cozy,
                   dedicate, distinctive, endorse, exact, fervor, foster, gifted,
                   gratify, heroism, indispensable, interest, knowledge, majestic,
                   mesh, nurture, palatial, polish, primarily, prosperity,
                   refine, rescue, safety, sensitive, soundness, suit, thrive,
                   understandable, vastness, wise, wonderful, workable,
                   world-famous, worthiness, worthy '''
positive_words = re.split(r',\s*', positive_words)
negative_words = re.split(r',\s*', profanity_words)
#all_data = dict(training_data, **held_data)
word_score_dict = ngoc_features.cheap_classifier(training_data)
keys = word_score_dict.keys()
def n_structural_features(sentence):
    dict_feature = {}
    sentence = nltk.word_tokenize(sentence)
    original_words = [w.rstrip(string.punctuation).lstrip(string.punctuation) for w in sentence]
    words_nosw = original_words[:]
    word_length =0
    all_cap_words = False #Number of words that are all caps
    begin_lower_case = 0 #Number of Words that are with beginning lower case.
    begin_upper_case = 0 #number of words that are beginning with upper case
    num_pos_words = 0 #Number of word that are positive
    num_neg_words = 0 #Number of Negative Words
    maybe =0
    total_word_scores = 0
    
    for word in original_words:
        if len(word)>0:
            if word in keys:
                total_word_scores += word_score_dict[word]
            if word.isupper():
                all_cap_words = True
            elif word[0].islower():
                begin_lower_case +=1
            elif word[0].isupper():
                begin_upper_case +=1
            if word in positive_words:
                num_pos_words +=1
            elif word in negative_words:
                num_neg_words +=1
            if word in stopwords.words('english'): #if a stopword
                words_nosw.remove(word)
            else:
                word_length+=len(word)

    if total_word_scores<-.75:
        average_score = -1
    elif total_word_scores<0.75:
        average_score = 0
    elif total_word_scores>.5:
        average_score = 1

    
    
    chars_per_word = word_length/(len(words_nosw)+1) #Average number of characters per word
    #print(chars_per_word)
    if chars_per_word <3.1:
        chars_per_word = 2
    elif chars_per_word <4.3:
        chars_per_word = 4
    else:
        chars_per_word = 5
        
    dict_feature['n_char_per_word'] = chars_per_word
    dict_feature['n_word_per_sentence'] = len(words_nosw)+1
    #dict_feature['n_all_cap_words'] = all_cap_words
    #dict_feature['n_num_uppper'] = begin_upper_case
    #dict_feature['n_num_lower'] = begin_lower_case
    #dict_feature['n_num_pos_words'] = num_pos_words
    #dict_feature['n_num_neg_words'] = num_neg_words
    dict_feature['n_average_score'] = average_score
    return dict_feature

#Structural Based Features Training
feature_sets = [(n_structural_features(n),g) for (n,g) in training_data.items()]
random.shuffle(feature_sets)
size = int(len(feature_sets)*0.9)
print "Training Data Set"

train_set, test_set = feature_sets[size:], feature_sets[:size]
classifier = nltk.DecisionTreeClassifier.train(train_set)
print nltk.classify.accuracy(classifier,test_set)
#classifier.show_most_informative_features()

print "Held Data Set"
test_set = [(n_structural_features(n), g) for (n,g) in held_data.items()]
print nltk.classify.accuracy(classifier, test_set)
#classifier.show_most_informative_features()

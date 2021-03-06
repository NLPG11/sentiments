# -*- coding: utf-8 -*-
from __future__ import division
import nltk, string, math, csv, parse, os, random, re, numpy

pos = set() 
neg =  set()
lit = set()
un = set() 
weak = set()
strong = set()

def csvload():
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
    for row in reader1:
        if len(row) == 1:
            pos.add(row[0].lower())
    for row in reader2:
        if len(row) == 1:
            neg.add(row[0].lower())
    for row in reader3:
        if len(row) == 1:
            lit.add(row[0].lower())
    for row in reader4:
        if len(row) == 1:
            un.add(row[0].lower())
    for row in reader5:
        if len(row) == 1:
            weak.add(row[0].lower())
    for row in reader6:
        if len(row) == 1:
            strong.add(row[0].lower())
csvload()


#train_base_path = "data/training/"
#train_files = ["Canon PowerShot SD500.txt", "Canon S100.txt", "Diaper Champ.txt", "Hitachi router.txt", "ipod.txt", "Linksys Router.txt", "MicroMP3.txt","Nokia 6600.txt", "norton.txt"]
#
#training_data = {}
#for train_file in train_files:
#    train_path = os.path.join(train_base_path, train_file)
#    parse.read_txt_data(train_path, training_data)
#
#held_base_path = "data/heldout/"
#held_files = ["Apex AD2600 Progressive-scan DVD player.txt", "Canon G3.txt", "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt", "Nikon coolpix 4300.txt", "Nokia 6610.txt"]
#
#held_data = {}
#for held_file in held_files:
#    held_path = os.path.join(held_base_path, held_file)
#    parse.read_txt_data(held_path, held_data)
#
#
#training_data = parse.val_to_polarity(training_data)
#held_data = parse.val_to_polarity(held_data)
#
''' Turney's Feature's list for the Gender Indentification paper gave us a basis
    for which features to look for. The group split up the features list. I took
    word features.
'''
''' Takes a string as an input. Tokenizes string into list.
    returns a dictionary with the following word features:
        -total number of words (n)
        -Average length per word (in characters) (avglen)
        -Vocabulary richness (total different words/N) (rich)
        -Words longer than 6 characters/N (longs)
        -Total number of short words (1-3 characters)/N (shorts)
        -Simpson’s D measure (SimpsonD)
        -Sichel’s S measure (SichelS)
        -Honore’s R measure (HonoreR)
        (LIWC was abandonned because of lack of access)
        -Wordstat features:
            -Negative (negemo)
            -Positive (posemo)
            -Uncertainty (uncertain)
            -Litigiousness (litig)
            -Weak Modal Words (weakModal)
            -Strong Modal Words (strongModal)


    '''

def sFeature(sent):
    sent = nltk.word_tokenize(sent)
    sent = [w.lower().rstrip(string.punctuation).lstrip(string.punctuation)  for w in sent]
            
    features = {}

    def basicFt(s):
        wc = len(s)
        if wc >= 40:
            features["wc"] = 5
        elif wc < 40 and wc >= 30:
            features["wc"] = 4       
        elif wc < 30 and wc >= 20:
            features["wc"] = 3       
        elif wc >= 10:
            features["wc"] = 2       
        else:
            features["wc"] = 1
            

        rich = 0
        if wc > 0:
            rich = len(set(s))/wc
        if rich > 0.667:
            features["rich"] = 3
        elif rich > 0.333 and rich < 0.667:
            features["rich"] = 2
        else:
            features["rich"] = 1

        avglen = 0
        longs = 0
        shorts= 0
        for w in s:
            if len(w) > 6:
                longs += 1
            if len(w) < 4:
                shorts += 1
            avglen += len(w)

        if longs < 4:
            features["longs"] = 1
        if longs >= 4 and longs < 8:
            features["longs"] = 2
        if longs >= 8:
            features["longs"] = 3

        if shorts < 4:
            features["shorts"] = 1
        if shorts >= 4 and shorts < 10:
            features["shorts"] = 2
        if shorts >= 10 and shorts < 20:
            features["shorts"] = 3
        if shorts >= 20:
            features["shorts"] = 4

        if wc > 0:
            avglen = avglen/wc

        if avglen < 2:
            features["avglen"] = 1
        if avglen >= 2 and avglen < 3:
            features["avglen"] = 2
        if avglen >= 3 and avglen < 3.5:
            features["avglen"] = 3
        if avglen >= 3.5 and avglen < 4:
            features["avglen"] = 4
        if avglen >= 4 and avglen < 5:
            features["avglen"] = 5
        if avglen >= 5:
            features["avglen"] = 6
        
    def sichelS(s):
        n = len(s)
        s2 = sorted(s)
        v2 = V(2, s2, n)
        if n > 0: 
            S = v2/n
        else:
            S = 0

        if S < 0.1 and S > 0:
            features["sichelS"] = 1
        elif S < 0.2 and S >= 0.1:
            features["sichelS"] = 2
        elif S >= 0.2 and S < 0.3:
            features["sichelS"] =  3
        elif S >= 0.3:
            features["sichelS"] =  4
        else: 
            features["sichelS"] = 0
                

    def V(num, s1, n):
        vm = 0
        for i in range(0, n-1):
            if i == 0:
                flag = False
                for j in range(0, num):
                    if s1[i] == s1[i + j]:
                        flag = True 
                    else:
                        flag = False 
                if flag == True:
                    vm += 1
            elif s1[i] != s1[i-1]:
                flag = False
                for j in range(0, num):
                    if i + j < n:
                        if s1[i] == s1[i + j]:
                            flag = True 
                        else:
                            flag = False 
                if flag == True:
                    vm += 1
        return vm
            
    def simpsonD(s):
        s1 = sorted(s)
        n = len(s)
        D = 0
        for m in range(1, n):
            D += V(m, s1, n) * (m / n) * ((m - 1)/(n-1))

        if D < 0.01 and D > 0:
            features["simpsonD"] = 1
        elif D >= 0.01 and D < 0.3:
            features["simpsonD"] =  2
        elif D >= 0.3 and D < 1:
            features["simpsonD"] =  3
        elif D >= 1:
            features["simpsonD"] =  4
        else: 
            features["simpsonD"] = 0



    def honoreR(s):
        n = len(s)
        s2 = sorted(s)
        v1 = V(1, s2, n) 
        if n > 0:
            R = 100 * (math.log(n)/ (1 - v1/n))
        else:
            R = 0
        if R < 1000:
            features["honoreR"] = 1
        if R < 2000 and R >= 1000:
            features["honoreR"] = 2
        if R < 3000 and R >= 2000:
            features["honoreR"] = 3
        if R > 3000:
            features["honoreR"] = 4
    
    def wordStat(s):
        posemo = 0
        negemo = 0
        uncertain = 0
        litig = 0
        weakModal = 0
        strongModal = 0
        for w in s:
            if w in pos:
                posemo += 1
            if w in neg:
                negemo += 1
            if w in lit:
                litig += 1
            if w in un:
                uncertain += 1
            if w in weak:
                weakModal += 1
            if w in strong:
                strongModal += 1
        if negemo >= 3:
            features["negemo"] = 3
        elif negemo >= 1 and negemo < 3:
            features["negemo"] = 2
        else:
            features["negemo"] = negemo 

        if posemo >= 3:
            features["posemo"] = 3
        elif posemo >= 1 and posemo < 3:
            features["posemo"] = 2
        else:
            features["posemo"] = posemo 

        if uncertain >= 3:
            features["uncertain"] = 3
        elif uncertain >= 1 and uncertain < 3:
            features["uncertain"] = 2
        else:
            features["uncertain"] = uncertain 

        if litig >= 3:
            features["litig"] = 3
        elif litig >= 1 and litig < 3:
            features["litig"] = 2
        else:
            features["litig"] = litig 

        if weakModal >= 3:
            features["weakModal"] = 3
        elif weakModal >= 1 and weakModal < 3:
            features["weakModal"] = 2
        else:
            features["weakModal"] = weakModal 

        if strongModal >= 3:
            features["strongModal"] = 3
        elif strongModal >= 1 and strongModal < 3:
            features["strongModal"] = 2
        else:
            features["strongModal"] = strongModal 
    
    basicFt(sent)
    wordStat(sent)
    honoreR(sent)
    sichelS(sent)
    simpsonD(sent)
    return features 

##testing
#feature_sets = [(sFeature(n), v) for (n,v) in training_data.items()]
#random.shuffle(feature_sets)
#size = int(len(feature_sets) * 0.9)
#print "training results"
#train_set, test_set = feature_sets[size:], feature_sets[:size]
##train_set = [line for line in train_set if line]
#
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, test_set)
#classifier.show_most_informative_features()
#
#print " heldout results"
#train_set = feature_sets
#test_set = [(sFeature(n), v) for (n,v) in held_data.items()]
#print nltk.classify.accuracy(classifier, test_set)
#classifier.show_most_informative_features()

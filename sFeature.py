# -*- coding: utf-8 -*-
from __future__ import division
import nltk, string, math

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

        -Yule’s K measure (YuleK)

        -Simpson’s D measure (SimpsonD)

        -Sichel’s S measure (SichelS)

        -Honore’s R measure (HonoreR)

        -Entropy measure (ent)
        
        (Avoided for now due to degree of tedium)
        -The number of net abbreviation /N (abbr)
        
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
        features["wc"] = wc       

        rich = len(set(s))/wc
        features["rich"] = rich

        avglen = 0
        longs = 0
        shorts= 0
        for w in s:
            if len(w) > 6:
                longs += 1
            if len(w) < 4:
                shorts += 1
            avglen += len(w)
        features["longs"] = longs
        features["shorts"] = shorts 
        avglen = avglen/wc
        features["avglen"] = avglen
        
#    def yuleK(s)
#        features["yuleK"] = yK
    def sichelS(s):
        n = len(s)
        v2 = 0
        s2 = sorted(s)
        for i in range (0, n-1):
            if i == 0:
                if s2[i] == s2[i+1] and s2[i] != s2[i+2]:
                    v2 += 1
            elif s2[i] == s2[i+1] and s2[i] != s2[i-1] and s2[i] != s2[i+2]:
                    v2 += 1
        S = v2/n
        features["sichelS"] = S
            
    def simpsonD(s):
        s1 = sorted(s)
        n = len(s)
        D = 0

        def V(num):
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

        for m in range(1, n):
            D += V(m) * (m / n) * ((m - 1)/(n-1))
                        
        features["simpsonD"] = D


    def honoreR(s):
        n = len(s)
        v1 = n 
        s2 = sorted(s)
        for i in range(0, n-1):
            if i == 0:
                if s2[i] == s2[i+1]:
                    v1 -= 2
            else:
                if s2[i] == s2[i+1] and s2[i] != s2[i-1]:
                    v1 -= 2 
                elif s2[i] == s2[i+1]:
                    v1 -= 1
        R = 0
        try:
            R = 100 * (math.log(n)/ (1 - v1/n))
        except ZeroDivisionError:
            print "divide by zero"
        features["honoreR"] = R 
    
#    def wordStat(s):
    
    print(sent)
    basicFt(sent)
    honoreR(sent)
    sichelS(sent)
    simpsonD(sent)
    return features 

print(sFeature("Ol dirty bastard put my foot in your uh."))

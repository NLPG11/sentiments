# -*- coding: utf-8 -*-
from __future__ import division
import nltk, string


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

        -LIWC features:
            Linguistic Processes:
            -dictionary words (dic)
            -Total function words (funct)
                -Total pronouns (pronoun)
                    -Personal pronouns (ppron)
                        -1st pers singular (i)
                        -1st pers plural (we)
                        -2nd person (you)
                        -3rd pers singular (shehe)
                        -3rd pers plural (they)
                    -Impersonal pronouns (ipron)
                -Articles (article)
                -Common verbs (verb)
                -Past tense (auxverb)
                -Present tense (present)
                -Future tense (future)
                -Adverbs (adverb)
                -Prepositions (prep)
                -Conjunctions (conj)
                -Negations (negate)
                -Quantifiers (quant)
                -Numbers (number)
                -Swear words (swear)
            Psychological Proccesses:
            -Social processes (social)
                -Family (family)
                -Friends (friend)
                -Humans (human)
            -Affective processes (affect)
                -Positive emotion (posemo)
                -Negative emotion (negemo)
                -Anxiety (anx)
                -Anger (anger)
                -Sadness (sad)
            -Cognitive processes (cogmech)
                -Insight (insight)
                -Causation (cause)
                -Discrepancy (discrep)
                -Tentative (tentat)
                -Certainty (certain)
                -Inhibition (always, never)
                -Inclusive (incl)
                -Exclusive (excl)
            -Perceptual processes (percept)
                -See (see)
                -Hear (hear)
                -Feel (feel)
            -Biological processes (bio)
                -Body (body)
                -Health (health)
                -Sexual (sexual)
                -Ingestion (ingest)
            -Relativity (relativ)
                -Motion (motion)
                -Space (space)
                -Time (time)
            Personal Concerns:
            -Work (work)
            -Achievement (achieve)
            -Leisure (leisure)
            -Home (home)
            -Money (money)
            -Religion (relig)
            -Death (death)
            Spoken categories:
            -Assent (assent)
            -Nonfluencies (nonflu)
            -Fillers (filler)


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
        
##    def yuleK(s)
##        features["yuleK"] = yK
##    def sichelS(s)
##        features["sichelS"] = sS
##    def simpsonD(s)
##        features["simpsonD"] = sD
##    def honoreR(s)
##        features["honoreR"] = hR
    
    def lingProc(s):
       #is dictionary word

        funct = 0
        prounoun = 0
        ppron = 0
        i = 0
        we = 0
        you = 0
        shehe = 0
        they = 0
        ipron = 0

        article = 0
        verb = 0
        auxverb = 0
        present = 0
        future = 0
        adverb = 0
        prep = 0
        conj = 0
        negate = 0
        quant = 0
        number = 0
        swear = 0

        for w in s:
            if w == "i":
                i += 1
            if w == "we" or w == "us" or w == "our":
                we += 1
            if w == "you" or w == "your" or w == "thou":
                you += 1
            if w == "she" or w == "he" or w == "him" or w == "her":
                you += 1
            if w == "they" or w == "their" or w == "they'd" or w == "them":
                they += 1
            if w == "it" or w == "it's" or w == "those":
                ipron += 1
            if w == "a" or "an" or w == "the":
                article += 1
        ppron = i + we + you + shehe + they
        pronoun = ppron + ipron
        features["pronoun"] = pronoun
        features["ppron"] = ppron
        features["ipron"] = ipron
        features["i"] = i
        features["we"] = we
        features["you"] =  you
        features["shehe"] = shehe 
        features["they"] = they
        
##    def psychProc(s)
        
##    def persConc(s)
        
##    def spokenCat(s)
    
    print(sent)
    basicFt(sent)
    lingProc(sent)
    return features 

#print(sFeature("Ol dirty bastard gonna fuck your ass up"))

from __future__ import division

import nltk, numpy
import parse
import re
import random
import nltk
import os


'''(ii)Feature format: We will use dict as our feature formats. In order to avoid key name collision, we will add our initial plus underschore in front of each key. ("t_len_sent" etc). More over, we will also normalize numeral values. Because the dictionaries won't have key collision, combining the them will be fairly straight forward.
Training data format is also a dictionary. It will consist of the sentence, plus the positive / negative sentiments associated with the dictionary. i.e. #<"I hate ipods":-2, "Music quality is great":2> etc. Moreoever, it is up to the individual to convert the vallues to polarity (though a helper function is available in parser.py.
'''



# train_base_path = "data/training/"
# train_files = ["Canon PowerShot SD500.txt", "Canon S100.txt", "Diaper Champ.txt", "Hitachi router.txt", "ipod.txt", "Linksys Router.txt", "MicroMP3.txt","Nokia 6600.txt", "norton.txt"]

# training_data = {}
# for train_file in train_files:
#     train_path = os.path.join(train_base_path, train_file)
#     parse.read_txt_data(train_path, training_data)


# held_base_path = "data/heldout/"
# held_files = ["Apex AD2600 Progressive-scan DVD player.txt", "Canon G3.txt", "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt", "Nikon coolpix 4300.txt", "Nokia 6610.txt"]

# held_data = {}
# for held_file in held_files:
#     held_path = os.path.join(held_base_path, held_file)
#     parse.read_txt_data(held_path, held_data)


# training_data = parse.val_to_polarity(training_data)
# held_data = parse.val_to_polarity(held_data)


#(i)
''' Takes a string as an input. Tokenizes string into list.
    returns a dictionary with the following word features:

h_determiner, h_conjunction, h_interjection, h_adjective, h_adjective_comparitive, h_adjective_superlative, h_adverb, h_adverb_comparitive, h_adadverb_superlative, h_gender_specific, h_female_specific, h_male_specific
as well as the 0/1 existance of each of these. 
'''
def get_function_features(sent):
	func_feats = {}
	func_feats['h_determiner'] = 0 
	func_feats['h_conjunction'] = 0 
	func_feats['h_interjection'] = 0 
	func_feats['h_adjective'] = 0 
	func_feats['h_adjective_comparitive'] = 0 
	func_feats['h_adjective_superlative'] = 0 
	func_feats['h_adverb'] = 0
	func_feats['h_adverb_comparitive'] = 0 
	func_feats['h_adverb_superlative'] = 0
	func_feats['h_gender_specific'] = 0
	func_feats['h_female_specific'] = 0
	func_feats['h_male_specific'] = 0

	female_words = set(["she", "her","herself"])
	male_words = set(["he", "him","himself"])
#use backoff tagger 

	text = nltk.word_tokenize(sent)
	pos = nltk.pos_tag(text)
	for word in pos:
		if word[0] in female_words:
			t = 0
			#func_feats['h_female_specific'] +=1
			#func_feats['h_gender_specific'] += 1
		elif word[0] in male_words:
			func_feats['h_male_specific'] +=1
			func_feats['h_gender_specific'] += 1
		if word[1] =='DT':
			func_feats['h_determiner']+=1
		elif word[1] =='CC' or word[1] =='IN':
			func_feats['h_conjunction'] +=1
		elif word[1] =='UH':
			func_feats['h_interjection'] +=1
		elif word[1] =='JJ':
			func_feats['h_adjective'] +=1
		elif word[1] =='JJR':
			func_feats['h_adjective_comparitive']+=1
			func_feats['h_adjective'] +=1
		elif word[1] =='JJS':
			func_feats['h_adjective_comparitive']+=1
			func_feats['h_adjective'] +=1
		elif word[1] =='RB':
			func_feats['h_adverb'] +=1
		elif word[1] =='RBR':
			func_feats['h_adverb_comparitive']+=1
			func_feats['h_adverb'] +=1
		elif word[1] =='RBS':
			func_feats['h_adverb_superlative']+=1
			func_feats['h_adverb'] +=1

	values = func_feats.values()
	min_val = min(values)
	max_val = max(values)+.000001
	for key in func_feats.keys():
		func_feats[key+"_normalized"]= (func_feats[key]-min_val)/(max_val-min_val) 
		if func_feats[key] >0:
			func_feats[key+"_exists"] = 1
		else: 
			func_feats[key+"_exists"] = 0

	'''
	(iii) You must show for each feature that you tried to optimize it; for example, if you used unigrams, you tested for the effects of using stopwords and/or stemming, or for example for bigrams you tested for informative collocations (e.g., using mutual information or chi-square or likelihood ratio, etc) or part of speech patterns a la Turney.
	for each feature, I considered both the original and normalized feature. I also considered if it was best to just check for the existence of that feature in the sentence. 

	I only included the best features in the dictonary I used


	adjective_superlative, was the same accross all 3
	adverb_exists was the highest
	adjective_comparitive_exists and adjective_comparitive were the same
	h_adjective_exists was the highest
	h_female_specific_exists and h_female_specific were the same
	h_determiner_exists was the highest
	h_adverb_superlative was the same accross all 3
	h_male_specific was the same accross all 3
	h_interjection was the same accross all 3 
	h_gender_specific was the same accross all 3 
	h_conjunction_exists was the highest
	h_adverb_comparitive and h_adverb_comparitive_normalized
	'''
	best_func_feats = {}
	
	best_func_feats['h_adverb_exists'] = func_feats['h_adverb_exists']
	best_func_feats['h_adjective_comparitive'] = func_feats['h_adjective_comparitive'] 
	best_func_feats['h_adjective'] = func_feats['h_adjective'] 
	best_func_feats['h_female_specific'] = func_feats['h_female_specific'] 
	best_func_feats['h_determiner_exists'] = func_feats['h_determiner_exists']
	best_func_feats['h_adverb_superlative'] = func_feats['h_adverb_superlative']
	best_func_feats['h_male_specific'] = func_feats['h_male_specific'] 
	
	best_func_feats['h_interjection'] = func_feats['h_interjection'] 
	best_func_feats['h_gender_specific'] = func_feats['h_gender_specific'] 
	best_func_feats['h_conjunction_exists'] = func_feats['h_conjunction_exists'] 

	best_func_feats['h_adverb_comparitive'] = func_feats['h_adverb_comparitive' ] 
	#return best_func_feats
	return func_feats






 
# #testing
# feature_sets = [(get_function_features(n), v) for (n,v) in training_data.items()]
# random.shuffle(feature_sets)
# size = int(len(feature_sets) * 0.9)
# print "trainging results"
# train_set, test_set = feature_sets[size:], feature_sets[:size]
# #train_set = [line for line in train_set if line]


# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print nltk.classify.accuracy(classifier, test_set)
# classifier.show_most_informative_features()

# print " heldout results"
# train_set = feature_sets
# test_set = [(get_function_features(n), v) for (n,v) in held_data.items()]
# print nltk.classify.accuracy(classifier, test_set)
# classifier.show_most_informative_features()

# #loop though each feature individually...
		
# classifier=[]
# feature_sets_keys =  feature_sets[0][0].keys()
# for i in range(36):
# 	print i
# 	feature_seti = [({feature_sets_keys[i]: n[feature_sets_keys[i]]}, v )for (n,v) in feature_sets]
# 	random.shuffle(feature_seti)
# 	size = int(len(feature_seti) * 0.9)
# 	print "trainging results"
# 	print feature_seti
# 	train_seti, test_seti = feature_seti[size:], feature_seti[:size]
# 	classifier += [nltk.NaiveBayesClassifier.train(train_seti)]
# 	print nltk.classify.accuracy(classifier[i], test_seti)
# 	classifier[i].show_most_informative_features()
# print feature_sets_keys
# test_set_keys = feature_sets_keys
# print " heldout results"
# i = 0
# for i in range (36):
# 	print i
# 	print test_set_keys[i]
# 	test_seti = [({test_set_keys[i]: n[test_set_keys[i]]}, v )for (n,v) in test_set]
# 	print nltk.classify.accuracy(classifier[i], test_seti)
# 	classifier[i].show_most_informative_features()




#Each individual feature must be tried out on the classification task to see how well it performs on the training data and on the held-out data. (iv) These results must be reported and included in the writeup. It is expected that each person individually is able to write code to run and test the classifier in this manner on the features they produce
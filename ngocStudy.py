import nltk
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
import random

def bigram_word_feats(words, score_fn=BigramAssocMeasures.likelihood_ratio, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] =(word in document_words)
    return features

def pos_features(word):
    features = {}
    for suffix in common_sufixes:
        features['endwith(%s)' % suffix] = word.lower().endswith(suffix)
    return features
    
def compare_classifier():
    featuresets =[(document_features(d), c) for (d,c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)

    otherfeaturesets = [(bigram_word_feats(d), c) for (d,c) in documents]
    train_set, test_set = otherfeaturesets[100:], otherfeaturesets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)


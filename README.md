TEST SET

We have decided not to assess how well you determine product attributes, since they were developed pretty arbitrarily in the test data. Instead, we are only evaluating on accuracy of sentiment polarity for each sentence. That said, when we judge the sentiment, we will be judging it according to what the person meant about the product or product attribute under discussion. So if the overall review of a camera, say, is positive, but a given sentence is negative about an attribute like the display, then the correct response is to mark that sentence as negative. We are not distinguishing between degrees of positive or negative; that is, between +1, +2, +3, etc., in the test set. Your score can be either +1 for positive, 0 for neutral, or -1 for negative. We will not include sentences that are both positive and negative in the test set.
Also, feel free to try to recognize product attributes in the test data if that can help you better determine sentiment polarity.

The test set we are developing will be similar in format and content to what you are training on.
There will be files named after the target product and the format of the lines will be similar, but not identical. The main differences are:

    No product attributes will be provided
    No sentiment scores will be provided
    A line number will be provided at the start of every line (before ## and [t])
    No lines will start with *

We will provide a sample file soon.
OUTPUT FILES

We want to make it easy to run our code to assess program, so we are going to follow the method used by competitions like TREC. Rather than having us load your code and run it, instead, we will ask you to process our test file and produce output in a standard format. We will then load that output file into our evaluation code and test that. To make the testing go smoothly, everyone needs to produce the output file in a very systematic way.

You will be need to produce one output file for all of the input files. That file must be of the following format to be correct:

product_name \t line_number \t sentiment_polarity \n

where

    product_name is the name of the file supplied with no leading or trailing white space, e.g., product2.txt
    line_number is the line number at the start of the line
    sentiment_polarity is either -1, 0, or 1 depending on if your algorithm thinks the sentence has negative, positive, or neutral sentiment
    each of these are separated by tabs (and no other whitespace, the spaces are shown above for readability) and each line is ended with a newline
    all lines for a given product file must appear consecutively in ascending order
    product file names should appear in alphabetical order

Name your file g_yourgroupnumber_output.txt

So an appropriate output file would look something like this, assuming there were three input files named product1.txt, product2.text, and product3.text, and the first had 4 lines, the second had 3 lines, and the third had 3 lines.

product1.txt 1 0
product1.txt 2 0
product1.txt 3 -1
product1.txt 4 1
product2.txt 1 1
product2.txt 2 0
product2.txt 3 -1
product3.txt 1 1
product3.txt 2 1
product3.txt 3 0


Sample test files and a sample output file: zip file.
 

COMPETITION RULES

You should use the classifiers in NLTK (or write your own) and not new plugins, so people don't spend time playing "find the best plugin".

You can train on data outside of the supplied corpora if you like.

You must be ready to run your classifier by 10am on Wednesday.

There is no time limit on how long it takes to train your classifier; however because we are going to evaluate everyone's algorithm in class on Wednesday, there is a time limit on how long it takes to run on new data.  It should take no more than 5 minutes to process 100 sentences (and this is a very generous estimate). If your classifier does take a long time to train, then you should train it before class and store the model to be loaded up during class (you can use cPickle for this as described in Chapter 5 if necessary).

Scoring: your algorithm will be scored on how well it does on a sentence-by-sentence basis.  Thus it needs to make a prediction for every sentence except for titles.  Scoring will be in terms of accuracy: number correct out of total number of sentences.

TO TURN IN ON MONDAY

Below, each item that must be turned in is preceded with a lowercase roman numeral.

Each person must individually develop at least one feature to be used by the group.

It is up to your group to determine who does what, but each individual must develop at least one distinct feature. Your group must also agree in advance how each individual should output the features so that they can be combined into the classifier. 
    (i) Each individual's code should be in the form of functions that produce output in this agreed-upon format and
    (ii) to get full credit the code must state what this format is in their documentation.
    (iii) You must show for each feature that you tried to optimize it; for example, if you used unigrams, you tested for the effects of using stopwords and/or stemming, or for example for bigrams you tested for informative collocations (e.g., using mutual information or chi-square or likelihood ratio, etc) or part of speech patterns a la Turney.

Each individual feature must be tried out on the classification task to see how well it performs on the training data and on the held-out data.
    (iv) These results must be reported and included in the writeup. It is expected that each person individually is able to write code to run and test the classifier in this manner on the features they produce.

Here are some distinct types of features to try:

-- a feature using parts-of-speech in some manner
-- a feature using regular expressions in some manner (with at least three rules)
-- a feature that tries to use bigrams in some manner;
-- using WordNet or some other lexicon

Here are variations to try:
-- counts vs. just presence of a feature
-- normalizing scores across features
-- careful tokenization

 
TO TURN IN ON WEDNESDAY:

Wednesday's assignment you'll turn in during class. This will be turned in as a group (I believe Canvas provides a way to do this and I will set up a separate assignment page for this).
Group code has to do several things:

-- Has to train a model
-- Has to use training data and held out data
-- Must only use classifiers supplied with NLTK
-- Should treat held out data properly (to assess your model, not to learn details)
-- Can optionally do cross-validation on the training set
-- Must produce an output file for evaluation of the appropriate format for the test data
-- Must be able to classify 100 test sentences in 5 minutes or fewer

You must turn in a file with the group code all together in one file, including all the feature extractor code. If you have trained a pickled a model, please upload that as well. Also upload the output file that is created by your code on the test set that we will provide in class.  

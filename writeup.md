Feature format:
We will use dict as our feature formats. In order to avoid key name collision, we will add our initial plus underschore in front of each key. ("t_len_sent" etc). More over, we will also normalize numeral values. Because the dictionaries won't have key collision, combining the them will be fairly straight forward.

Training data format is also a dictionary. It will consist of the sentence, plus the positive / negative sentiments associated with the dictionary. i.e. #<"I hate ipods":-2, "Music quality is great":2> etc. Moreoever, it is up to the individual to convert the vallues to polarity (though a helper function is available in parser.py.


**Tristan**:
I developed the parser that reads in the files and creates the data format. parser.usage_contains.py contains the sample code that utilizes parse.py. I've also included a few helper functions that may be helpful in parser.py

Before I started testing, I tried to determine whether testing with raw sentiment values (-3, -2 -1, 0, 2,.. etc) was better than polarity (-1, 0, 1). Unsurprisingly, testing with polarity offered better results. All testing below were done based on polarity prediction (as specified by the competition spec)

While testing my features, I first tried the following features as char_based_features.

    F1 total number of characters in words(C)
    F2 total number of letters(a-z)/C
    F3 total number of upper characters/C
    F4 total number of digital characters/C
    F5 total number of white-space characters/C
    F6 total number of tab space characters/C
    F7 : : : F29 number of special characters(%,etc.)/C(23 features)
    
In order to optimize for the features, I tried the classification by holding a feature out, to asses weather the percentage improved. The original classfication achieved roughly 52% accuracy. After some tweaking, I achieved 54% accuracy

In addition to the above feature, I also tried the following features as syntactic_features:

    #F131 number of single quotes(')/C
    F133 number of periods(.)/C
    F134 number of colons(:)/C
    F135 number of semi-colons(;)/C
    F136 number of question marks(?)/C
    F138 number of exclamation marks(!)/C
    F140 number of ellipsis(. . . ) /C
    
I applied the same technique in optimizing the features. I started out with roughly 54% accuracy. After some tweaking, I was able to increase the accuracy to 59% (namel leaving out semi-colons, exclamation marks, and Ellipses.



**Spencer**:

**Ngoc**:

**Huda**:

import sys
import re

def add_data(training, temp_feat):
    one = temp_feat[0]
    one = one.replace("}", "]")
    try:
        val = int(re.search('\[(.*?)\]', one).group(1))
    except TypeError as tE:
        print "Couldn't parse sentiment value"
        sys.exit()
    except IndexError as iE:
        print "Index error"
        print one
        print re.findall('\[(.*)\]', one)
        sys.exit()
    except ValueError as vE:
        print "Value Error"
        re.match('\[(.*)\]', one)
        print re.search('\[(.*)\]', one).groups()
        sys.exit()
    except AttributeError as aE:
        print "Attribute Error"
        print one
        print training_data
        sys.exit()
    for index in xrange(0, len(temp_feat)):
        target = temp_feat[index]
        remove = re.search("(.*##)", target)
        #This will actually remove the ## part of the review as well
        if not remove is None:
            target = target.replace(remove.group(1), "").strip() #remove the head
        training[target] = val

def read_txt_data(path, training_data):
    text_file = open(path, "r")
    temp_features = []
    new_sent_val = False
    for line in text_file:
        #print line
        if (len(re.findall(r"\[[\+|\-][0-9]\]+", line)) >= 1) and not new_sent_val: #new one
            temp_features.append(line)
            new_sent_val = True
            continue
        elif (len(re.findall(r"\[[\+|\-][0-9]\]+", line)) >= 1) and new_sent_val: #end
            add_data(training_data, temp_features) #Do the work,
            temp_features = []
            temp_features.append(line)
            new_sent_val = True
            continue
        if new_sent_val:
            temp_features.append(line)
    add_data(training_data, temp_features) #last one, corner case



#print len(training_data)
#print training_data




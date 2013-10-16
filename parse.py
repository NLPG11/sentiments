import sys
import re

def add_data(training, temp_feat):
    '''
    given the list of sentences, it assigns them all the same value
    extracted from the product sentiment.
    '''
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
        #sys.exit()
        return
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
    #print val

def val_to_polarity(training_data):
    '''Given a training data, changes all vals (such as -2, -1, 0, 1, 4) 
    into polarity (-1, 0, 1).
    '''
    new_data = {}
    for k, v in training_data.items():
        if v == 1 or v == 0:
            new_data[k] = 0
        elif v > 1:
            new_data[k] = 1
        else:
            new_data[k] = -1
    return new_data


def read_txt_data(path, training_data):
    '''
    Given the path to the training file, it fills the training_data 
    dict with the appropriate sentence to sentiment pair.
    '''
    text_file = open(path, "r")
    temp_features = []
    new_sent_val = False
    for line in text_file:
        if "[t]" in line:
            continue
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


def read_test_data(path):
    '''
    Reads the test files, returns a dict of number to sentences
    '''
    text_file = open(path, "r")
    temp_dict = {}
    keys_list = []
    val_list = []
    for line in text_file:
        sep = line.split("\t")
        #temp_dict[sep[0]] = sep[1].strip().replace("##", "")
        keys_list.append(sep[0])
        val_list.append(sep[1].strip().replace("##", ""))
    return keys_list, val_list
    #return temp_dict



def rangefy(v):
    ret = None
    if v == 0 or v == 1:
        ret = 0
    elif v > 1:
        ret = 1
    else:
        ret = -1
    return ret

#parse.read_test_data("sampleOutput/product1.txt")

#print len(training_data)
#print training_data





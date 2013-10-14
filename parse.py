import sys
import re

text_file = open("data/training/ipod.txt", "r")
kill = 0
new_feature_flag = False

training_data = {} #<sentence:sent_num>, i.e. <"I love it!":3>

temp_features = []
new_sent_val = False

def add_data(training, temp_feat):
    one = temp_feat[0]
    one = one.replace("}", "]")
    try:
        val = int(re.search('\[(.*?)\]', one).group(1))
    except TypeError as tE:
        print "Couldn't parse sentiment value"
    except IndexError as iE:
        print "Index error"
        print one
        print re.findall('\[(.*)\]', one)
    except ValueError as vE:
        print "Value Error"
        re.match('\[(.*)\]', one)
        print re.search('\[(.*)\]', one).groups()
    except AttributeError as aE:
        print "Attribute Error"
        print one
        print training_data
        sys.exit()
    for index in xrange(0, len(temp_feat)):
        training[temp_feat[index]] = val


for line in text_file:
    print line
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
    if kill >= 10000:
        break
    kill += 1

add_data(training_data, temp_features) #last one, corner case

print len(training_data)
print training_data
print debug_list
a = ["features[-2]## There isn't much features on the iPod at all, except games"]
add_data({}, a)




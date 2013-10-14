import parse

print "Starting usage sample"

test_path = "data/training/ipod.txt"
training_data = {}

#Read the text and create data dict
parse.read_txt_data(test_path, training_data)

print len(training_data)

#You should be able to continuourly call the function with different path, 
#but with the same dictioary to build a comprehensive training dict.


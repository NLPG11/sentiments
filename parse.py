import sys
import re

text_file = open("data/training/ipod.txt", "r")
kill = 0
new_feature_flag = False

for line in text_file:
    if re.search("[\+|\-][0-9]+", line):
        print line
    if kill >= 10:
        sys.exit()
    kill += 1

lines = text_file.readlines()

print lines

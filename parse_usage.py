import parse
import os


print "Starting usage sample"

##################################TRAIN DATA ACUISITION########
train_base_path = "data/training/"
train_files = ["Canon PowerShot SD500.txt", "Canon S100.txt", "Diaper Champ.txt",
               "Hitachi router.txt", "ipod.txt", "Linksys Router.txt", "MicroMP3.txt",
              "Nokia 6600.txt", "norton.txt"]

training_data = {}

for train_file in train_files:
    train_path = os.path.join(train_base_path, train_file)
    parse.read_txt_data(train_path, training_data)

##################################HELD DATA ACUISITION########
held_base_path = "data/heldout/"
held_files = ["Apex AD2600 Progressive-scan DVD player.txt", "Canon G3.txt", "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt",
               "Nikon coolpix 4300.txt", "Nokia 6610.txt"]
held_data = {}

for held_file in held_files:
    held_path = os.path.join(held_base_path, held_file)
    parse.read_txt_data(held_path, held_data)

print len(training_data)
print len(held_data)

#!/usr/bin/python
# Name: 
# Date:
# Description:
#
#

# all divide operation will result in float number
from __future__ import division
from math import log
from porter2 import stem
from random import shuffle
import math, os, pickle, re, sys, time

def unique(words):
    i = 0
    j = 1
    length = 1
    while j < len(words):
        if words[i] == words[j]:
            j += 1
            continue
        else:
            words[i+1] = words[j]
            i += 1
            j += 1
            length += 1
    return length

class Bayes_Classifier:

    def __init__(self, file_list, directory, cross = False):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
        cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
        the system will proceed through training.  After running this method, the classifier 
        is ready to classify input text."""
        self.class_dict = {}
        self.positive_word = {}
        self.negative_word = {}
        if not cross:
            if os.path.exists("positive_word_best.pickle") and os.path.exists("negative_word_best.pickle") and os.path.exists("class_dict_best.pickle"):
                self.class_dict = self.load("class_dict_best.pickle")
                self.positive_word = self.load("positive_word_best.pickle")
                self.negative_word = self.load("negative_word_best.pickle")
            else:
                self.class_dict, self.positive_word, self.negative_word = self.train(file_list, directory)
        else:
            self.class_dict, self.positive_word, self.negative_word = self.train(file_list, directory, True)

        self.pos_num = self.class_dict["positive"]
        self.neg_num = self.class_dict["negative"]
        self.total_num = self.pos_num + self.neg_num

        self.prob_pos = self.pos_num / self.total_num
        self.prob_neg = self.neg_num / self.total_num

        self.pos_word_count = 0
        for word in self.positive_word:
            self.pos_word_count += self.positive_word[word]

        self.neg_word_count = 0
        for word in self.negative_word:
            self.neg_word_count += self.negative_word[word]

        words = []
        for word in self.positive_word:
            words.append(word)
        for word in self.negative_word:
            words.append(word)

        words.sort()

        self.voc_length = unique(words)
        #print self.voc_length
        #print self.pos_word_count
        #print self.neg_word_count

    def train(self, file_list, directory, cross = False):
        """Trains the Naive Bayes Sentiment Classifier."""
        class_dict = {}
        class_dict["positive"] = 0
        class_dict["negative"] = 0
        for file in file_list:
            if file == ".DS_Store":
                continue
            dot_index = file.index('.')
            file = file[:dot_index]
            splits = file.split('-')
            #print splits
            if splits[1] == '5':
                class_dict["positive"] +=1
            else:
                class_dict["negative"] += 1

        #word_dict = {}
        positive_word = {}
        negative_word = {}

        for file in file_list:
            dot_index = file.index('.')
            file_string = file[:dot_index]
            splits = file_string.split('-')

            file_name = directory + file
            sTxt = self.loadFile(file_name)
            tokens = self.tokenize(sTxt)

            if splits[1] == '5':
                for word in tokens:
                    word = stem(word)
                    if word not in positive_word:
                        positive_word[word] = 1
                    else:
                        positive_word[word] += 1
            else:
                for word in tokens:
                    word = stem(word)
                    if word not in negative_word:
                        negative_word[word] = 1
                    else:
                        negative_word[word] += 1

        if not cross:
            self.save(class_dict, "class_dict_best.pickle")
            self.save(positive_word, "positive_word_best.pickle")
            self.save(negative_word, "negative_word_best.pickle")

        return class_dict, positive_word, negative_word
     
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        tokens = self.tokenize(sText)
        
        prob = {}
        prob["positive"] = log(self.prob_pos, 2)
        prob["negative"] = log(self.prob_neg, 2)
    
        for c in self.class_dict:
            for word in tokens:
                word = stem(word)
                p = None
                if c == "positive":
                    if word in self.positive_word:
                        p = (self.positive_word[word] + 1) / (self.pos_word_count + self.voc_length)
                    else:
                        p = 1 / (self.pos_word_count + self.voc_length)

                else:
                    if word in self.negative_word:
                        p = (self.negative_word[word] + 1) / (self.neg_word_count + self.voc_length)
                    else:
                        p = 1 / (self.neg_word_count + self.voc_length)
                
                prob[c] += log(p, 2)
         
        if prob["negative"] > prob["positive"]:
            return "negative"
        elif prob["positive"] > prob["negative"]:
            return "positive"
        else:
            return "neutral"

    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt
    
    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()
    
    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText): 
        """Given a string of text sText, returns a list of the individual tokens that 
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[A-Z]", str(c)) != None:
                sToken += c.lower()
            elif re.match("[a-z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
               if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
               if c.strip() != "":
                    lTokens.append(str(c.strip()))
                 
        if sToken != "":
            lTokens.append(sToken)

        return lTokens

    def calAccuracy(self, test_file, directory):
        correct = 0
        for file in test_file:
            if file == ".DS_Store":
                continue
            sTxt = self.loadFile(directory + file)
            c = self.classify(sTxt)
            
            dot_index = file.index('.')
            file_string = file[:dot_index]
            splits = file_string.split("-")

            if splits[1] == '5' and c == "positive":
                correct += 1
            if splits[1] == '1' and c == "negative":
                correct += 1
        return correct / len(test_file)
            
            
 
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage:"
        print "./bayesbest.py:      : Using all data as training data, and testing data"
        print "./bayesbest.py -c    : Using 10 fold cross validation"
        print

    file_list = []
    directory = ""
    for item in os.walk("./movies_reviews/"):
        file_list = item[2]
        directory = item[0]
        break



    if len(sys.argv) == 1:
        print "Using all data as testing data"
        c_a = Bayes_Classifier(file_list, directory)
        #print "after training"
        accuracy = c_a.calAccuracy(file_list, directory)
        print "accuracy =", accuracy

    if len(sys.argv) == 2 and sys.argv[1] == "-c":
        average_accuracy = 0
        div = int(len(file_list) / 10)
        shuffle(file_list)
        for i in range(10):
            print "Using " + str(i) + "th fold as testing data"
            t1 = time.time()
            train_file = file_list[i*div+div:]
            train_file = train_file + file_list[:i*div]
            test_file = file_list[i*div: i*div + div]
            c = Bayes_Classifier(train_file, directory, True)
            accuracy = c.calAccuracy(test_file, directory)
            print "accuracy =", accuracy
            average_accuracy += accuracy
            print "%d seconds passed" % (time.time() - t1)
            print
        print "average_accuracy =", average_accuracy / 10

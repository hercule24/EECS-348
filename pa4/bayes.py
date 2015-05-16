#!/usr/bin/python
# Name: 
# Date:
# Description:
#
#

# all divide operation will result in float number
from __future__ import division
import math, os, pickle, re

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
        cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
        the system will proceed through training.  After running this method, the classifier 
        is ready to classify input text."""
        class_dict = {}
        self.positive_word = {}
        self.negative_word = {}
        if os.path.exists("positive_word.pickle")and os.path.exists("negative_word.pickle") and os.path.exists("class_dict.pickle"):
            class_dict = self.load("class_dict.pickle")
            self.positive_word = self.load("positive_word.pickle")
            self.negative_word = self.load("negative_word.pickle")
        else:
            class_dict, self.positive_word, self.negative_word = self.train()

        self.pos_num = class_dict["positive"]
        self.neg_num = class_dict["negative"]
        self.total_num = self.pos_num + self.neg_num

        self.prob_pos = self.pos_num / self.total_num
        self.prob_neg = self.neg_num / self.total_num

    def train(self):   
        """Trains the Naive Bayes Sentiment Classifier."""
        file_list = []
        directory = ""

        for item in os.walk("./movies_reviews/"):
            file_list = item[2]
            directory = item[0]
            break
        
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
                    if word not in positive_word:
                        positive_word[word] = 1
                    else:
                        positive_word[word] += 1
            else:
                for word in tokens:
                    if word not in negative_word:
                        negative_word[word] = 1
                    else:
                        negative_word[word] += 1

        self.save(class_dict, "class_dict.pickle")
        self.save(positive_word, "positive_word.pickle")
        self.save(negative_word, "negative_word.pickle")

        return class_dict, positive_word, negative_word
     
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

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
           if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
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

if __name__ == "__main__":
    c = Bayes_Classifier()

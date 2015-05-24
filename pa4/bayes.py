#!/usr/bin/python
# Name: 
# Date:
# Description:
#
#

# all divide operation will result in float number
from __future__ import division
from math import log
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
            if os.path.exists("positive_word.pickle")and os.path.exists("negative_word.pickle") and os.path.exists("class_dict.pickle"):
                self.class_dict = self.load("class_dict.pickle")
                self.positive_word = self.load("positive_word.pickle")
                self.negative_word = self.load("negative_word.pickle")
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

        if not cross:
            self.save(class_dict, "class_dict.pickle")
            self.save(positive_word, "positive_word.pickle")
            self.save(negative_word, "negative_word.pickle")

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

    def calAccuracy(self, file_list, directory):
        correct = 0
        # actual num of class examples
        pos_num = 0
        neg_num = 0

        # num of correctly classified examples
        pos_correct = 0
        neg_correct = 0
        
        # num of total classified examples
        pos_fake_num = 0
        neg_fake_num = 0

        for file in file_list:
            if file == ".DS_Store":
                continue
            sTxt = self.loadFile(directory + file)
            c = self.classify(sTxt)

            dot_index = file.index('.')
            file_string = file[:dot_index]
            splits = file_string.split("-")

            if splits[1] == '5':
                pos_num += 1
            if splits[1] == '1':
                neg_num += 1

            if c == "positive":
                pos_fake_num += 1
                if splits[1] == '5':
                    correct += 1
                    pos_correct += 1
            
            if c == "negative":
                neg_fake_num += 1
                if splits[1] == '1':
                    correct += 1
                    neg_correct += 1

        accuracy = correct / len(file_list)
        pos_precision = pos_correct / pos_fake_num
        pos_recall = pos_correct / pos_num
        f_pos = 2 * pos_precision * pos_recall / (pos_precision + pos_recall)
        neg_precision = neg_correct / neg_fake_num
        neg_recall = neg_correct / neg_num
        f_neg = 2 * neg_precision * neg_recall / (neg_precision + neg_recall)
        return accuracy, (pos_precision, pos_recall, f_pos), (neg_precision, neg_recall, f_neg)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage:"
        print "./bayesbest.py       : Using all data as training data, and testing data"
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
        accuracy, pos_tuple, neg_tuple = c_a.calAccuracy(file_list, directory)
        print "Total accuracy =", accuracy
        print "Positive precision = %f, positive recall = %f, positive f-measure = %f" % (pos_tuple[0], pos_tuple[1], pos_tuple[2])
        print "Negative precision = %f, negative recall = %f, negative f-measure = %f" % (neg_tuple[0], neg_tuple[1], neg_tuple[2])


    if len(sys.argv) == 2 and sys.argv[1] == "-c":
        total_accuracy = 0

        total_pos_precision = 0
        total_pos_recall = 0
        total_pos_f_measure = 0

        total_neg_precision = 0
        total_neg_recall = 0
        total_neg_f_measure = 0
    
        div = int(len(file_list) / 10)
        shuffle(file_list)
        for i in range(10):
            print "Using " + str(i) + "th fold as testing data"
            t1 = time.time()
            train_file = file_list[i*div+div:]
            train_file = train_file + file_list[:i*div]
            test_file = file_list[i*div: i*div + div]
            c = Bayes_Classifier(train_file, directory, True)

            accuracy, pos_tuple, neg_tuple = c.calAccuracy(test_file, directory)

            total_pos_precision += pos_tuple[0]
            total_pos_recall += pos_tuple[1]
            total_pos_f_measure += pos_tuple[2]

            total_neg_precision += neg_tuple[0]
            total_neg_recall += neg_tuple[1]
            total_neg_f_measure += neg_tuple[2]

            print "Total accuracy =", accuracy
            print "Positive precision = %f, positive recall = %f, positive f-measure = %f" % (pos_tuple[0], pos_tuple[1], pos_tuple[2])
            print "Negative precision = %f, negative recall = %f, negative f-measure = %f" % (neg_tuple[0], neg_tuple[1], neg_tuple[2])
            total_accuracy += accuracy
            print "%d seconds passed" % (time.time() - t1)
            print
        print "Average accuracy =", total_accuracy / 10
        print "Average positive precision = %f, average positive recall = %f, average positive f-measure = %f" % (total_pos_precision / 10, total_pos_recall / 10, total_pos_f_measure / 10)
        print "Average negative precision = %f, average negative recall = %f, average negative f-measure = %f" % (total_neg_precision / 10, total_neg_recall / 10, total_neg_f_measure / 10)

#!/usr/bin/python
import StrokeHmm

#states = ["Healthy", "Fever"]
#features = ["feeling"]
#featuresCorD = {"feeling" : StrokeHmm.DISCRETE}
#numVals = {"feeling" : 3}
#
#hmm = StrokeHmm.HMM(states, features, featuresCorD, numVals)
#hmm.priors = {"Healthy" : 0.6, "Fever" : 0.4}
#hmm.transitions = {"Healthy" : {"Healthy" : 0.7, "Fever" : 0.3}, "Fever" : {"Healthy" : 0.4, "Fever" : 0.6}}
#hmm.emissions = {"Healthy" : {"feeling" : [0.5, 0.4, 0.1]}, "Fever" : {"feeling" : [0.1, 0.3, 0.6]}}
#
#data = [{"feeling" : 0}, {"feeling" : 1}, {"feeling" : 2}]
#print hmm.label(data)


x = StrokeHmm.StrokeLabeler()
#print strokes
#print labels
x.trainHMMDir("../trainingFiles")
strokes, labels = x.loadLabeledFile("../trainingFiles/0128_1.6.1.labeled.xml")
print
print "true labels:"
print labels
print
prob, fake_labels = x.labelStrokes(strokes)
print "fake labels"
print fake_labels
print
print x.confusion(labels, fake_labels)

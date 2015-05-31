#!/usr/bin/python
import StrokeHmm

states = ["Sunny","Cloudy","Rainy"]
features = ["humidity"]
featuresCorD = {"humidity" : StrokeHmm.DISCRETE}
numVals = {"humidity":4}


hmm = StrokeHmm.HMM(states, features, featuresCorD, numVals)
hmm.priors = {"Sunny" : 0.63, "Cloudy" : 0.17, "Rainy" : 0.20}
hmm.transitions = {"Sunny" : {"Sunny" : 0.500, "Cloudy" : 0.375, "Rainy" : 0.125}, "Cloudy" : {"Sunny" : 0.250, "Cloudy" : 0.125, "Rainy" : 0.625}, "Rainy" : {"Sunny" : 0.250, "Cloudy" : 0.375, "Rainy" : 0.375}}
hmm.emissions = {"Sunny" : {"humidity" : [0.60, 0.20, 0.15, 0.05]}, "Cloudy" : {"humidity" : [0.25, 0.25, 0.25, 0.25]}, "Rainy" : {"humidity" : [0.05, 0.10, 0.35, 0.50]}}

data = [{"humidity" : 0}, {"humidity" : 1}, {"humidity" : 2}]
print hmm.label(data)

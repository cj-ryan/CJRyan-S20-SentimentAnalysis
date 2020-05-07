# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:05:47 2020

@author: CJ
"""

from flair.models import TextClassifier
from flair.data import Sentence

import pandas

classifier = TextClassifier.load('en-sentiment')

def getLabel(text):
    sentence = Sentence(str(text))
    classifier.predict(sentence)
    label = sentence.labels[0]
    if label.value == 'POSITIVE':
        return float(label.score)
    elif label.value == 'NEGATIVE':
        return -1*float(label.score)
    
def sentGraph(filepath):
    data = pandas.read_csv(filepath)
    
    data['sentiment'] = data['text'].apply(getLabel)
    
    data.to_csv(filepath[0:-4]+"_analyzed.csv", index=False)
    
    print("Done.")
    
def main():
    filepath = input("Please input a file path: ")
    sentGraph(filepath)
    
if __name__ == "__main__": 
    # calling main function 
    main() 
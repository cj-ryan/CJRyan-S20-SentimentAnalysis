#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 12:48:54 2020

@author: guest
"""

from flair.models import TextClassifier
from flair.data import Sentence

import pandas
import plotly.graph_objects as go

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
    
    #data = data.set_index(['time'])
    
    data['time'] = pandas.DatetimeIndex(data.time)
    
    fig = go.Figure(data=go.Scatter(x=data['time'],
                                    y=data['sentiment'],
                                    mode='markers',
                                    marker_color=data['sentiment'],
                                    text=data['text'])) # hover text goes here
    
    
    fig.update_layout(title='Coronavirus Twitter Sentiment Analysis')
    fig.show()
    
def main():
    filepath = input("Please input a file path: ")
    sentGraph(filepath)
    
if __name__ == "__main__": 
    # calling main function 
    main() 
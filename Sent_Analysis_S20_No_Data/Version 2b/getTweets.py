#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:42:56 2020

@author: guest
"""

import re 
import tweepy
#import plotly.graph_objects as go

import os
#import sys

from tweepy import OAuthHandler 
#from textblob import TextBlob 

#from wordcloud import WordCloud, STOPWORDS 
#import matplotlib.pyplot as plt 
import pandas as pd

import csv
import time

from datetime import datetime

# by CJ Ryan and John Johnson
#Tweet sets retreived with TweetSets

# TwitterClient class by Nikhil Kumar for GeeksForGeeks
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = '3ntqzQQsrBGhoMHRamwWyRGgZ'
        consumer_secret = 'bGAnSE4tENkNd5e0a2bkwlyhrDYGTSYmiJHOTZIYELNSNTap5r'
        access_token = '562358787-67yrbNshjlBTeZxiUzIDtNZdyN9SirltKOOGpCTp'
        access_token_secret = 'eX6cDln0QpWpjklu3hv7BF7gAhs68lWo1wWLdwDSH26Yc'

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


    def get_tweets(self, query, count = 100): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 

        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, lang = 'en', count = count) 

            # parsing tweets one by one 
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 

                #saving id of tweet
                parsed_tweet['id'] = tweet.id
                
                #saving text of tweet 
                parsed_tweet['text'] = self.clean_tweet(tweet.text)
                
                #saving date & time of tweet
                parsed_tweet['time'] = tweet.created_at
            

                # appending parsed tweet to tweets list 
                if (not tweet.retweeted) and ('RT @' not in tweet.text):
                    tweets.append(parsed_tweet)

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))
            
def saveTweetsOverTime(numPulls, timePerPull, topics, outfilename):
    api = TwitterClient()
    
    allTweets = []
    
    print("Getting tweets 1 of {}...".format(numPulls))
    
    for topic in topics:
        allTweets.append(api.get_tweets(query=topic))
    
    for x in range(numPulls-1):
        time.sleep(timePerPull)
        print("Getting tweets {} of {}...".format(x+2, numPulls))
        for topic in topics:
            allTweets.append(api.get_tweets(query=topic))
        
    
    with open('temp.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text', 'time'])
        for data in allTweets:
            for entry in data:
                writer.writerow([entry['id'], entry['text'], entry['time']])
                
    df = pd.read_csv("temp.csv")
    df.drop_duplicates(subset=None, inplace=True)
    df.to_csv(outfilename, index=False)
    os.remove("temp.csv")
    print("Done.")
    
    
        
def main():
    topics = ["coronavirus", "covid"]
    while(1):
        saveTweetsOverTime(5, 1, topics, "coronavirus_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv")

if __name__ == "__main__": 
    # calling main function 
    main() 
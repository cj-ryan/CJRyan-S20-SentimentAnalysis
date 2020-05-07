import re 
import tweepy
import plotly.graph_objects as go

import sys

from tweepy import OAuthHandler 
from textblob import TextBlob 

from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 


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

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment
                
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

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

                # saving text of tweet 
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))
            
def exportData(query):
    api = TwitterClient()
    tweets = api.get_tweets(query = query, count = 10000)
    
    if len(tweets) == 0:
            sys.exit("Insufficient live data.")
            
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets 
    percentPos = 100*len(ptweets)/len(tweets)
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets
    percentNeg = 100*len(ntweets)/len(tweets)
    # percentage of neutral tweets
    percentNeu = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
    
    return percentPos, percentNeu, percentNeg, len(tweets)

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets
    topics = []
    
    posTweets = []
    negTweets = []
    neuTweets = []
    
    while 1:
        topic = input("Enter the topic to be analyzed (or 'quit' to stop): ")
        if topic == 'quit':
            break
        tweets = api.get_tweets(query = topic, count = 10000)
        
        if len(tweets) == 0:
            print("\nInsufficient Data")
            continue
        print("\nOf {} tweets: ".format(len(tweets)))
        # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        # percentage of positive tweets 
        percentPos = 100*len(ptweets)/len(tweets)
        print("Positive tweets percentage: {} %".format(percentPos))
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets
        percentNeg = 100*len(ntweets)/len(tweets)
        print("Negative tweets percentage: {} %".format(percentNeg))
        # percentage of neutral tweets
        #neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        percentNeu = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
        print("Neutral tweets percentage: {} % ".format(percentNeu))
        
    
        # printing first 5 positive tweets 
        print("\nPositive tweets:") 
        for tweet in ptweets[:10]: 
            print(tweet['text']) 
    
        # printing first 5 negative tweets 
        print("\n\nNegative tweets:") 
        for tweet in ntweets[:10]: 
            print(tweet['text'])
        
        '''
        print("\n\nNeutral tweets:")
        for tweet in neutweets[:10]: 
            print(tweet['text']) 
        '''
            
        print("\n============================================")
        if percentNeg == 0:
            print("\nThe topic \"{}\" has no negative tweets.".format(topic))
        elif percentPos == 0:
            print("\nThe topic \"{}\" has no positive tweets.".format(topic))
        elif percentPos/percentNeg > 1.6:
            print("\nThe topic \"{}\" has a strong positive sentiment.".format(topic))
        elif percentPos/percentNeg > 1.2:
            print("\nThe topic \"{}\" has a weak positive sentiment.".format(topic))
        elif percentNeg/percentPos > 1.6:
            print("\nThe topic \"{}\" has a strong negative sentiment.".format(topic))
        elif percentNeg/percentPos > 1.2:
            print("\nThe topic \"{}\" has a weak negative sentiment.".format(topic))
            
        else:
            print("\nThe topic \"{}\" is controversial.".format(topic))
        
        print("\n============================================\n")
        
        topics.append(topic)
        
        posTweets.append(len(ptweets))
        negTweets.append(len(ntweets))
        neuTweets.append((len(tweets) - len(ntweets) - len(ptweets)))

        
        fig = go.Figure(data=[
        go.Bar(name='negative', x=topics, y=negTweets, marker={'color':'red'}),
        go.Bar(name='neutral', x=topics, y=neuTweets, marker={'color':'lightgrey'}),
        go.Bar(name='positive', x=topics, y=posTweets, marker={'color':'lightgreen'}),
        ])
        # Change the bar mode
        fig.update_layout(barmode='stack')
        fig.show()
        
        content = ' '
        stopwords = set(STOPWORDS)
        for tweet in tweets:
            val = tweet['text']
            tokens = val.split()
            for words in tokens:
                content = content + words + ' '
        
        wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(content)
        
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
  
        plt.show() 
        
if __name__ == "__main__": 
    # calling main function 
    main() 

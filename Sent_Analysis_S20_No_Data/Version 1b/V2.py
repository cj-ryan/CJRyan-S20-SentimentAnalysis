import re 
import plotly.graph_objects as go
import csv

import sys


from textblob import TextBlob 


# by CJ Ryan and John Johnson
#Tweet sets retreived with TweetSets


def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment
                
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'


def getTweets(topic):
    relevantTweets = []
    with open('vaccinetweets2.csv',encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
            
        for row in csv_reader:
            parsed_tweet = {}
            parsed_tweet['text'] = row[17]
            if topic in parsed_tweet['text'] and not row[14]:
                parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text'])
                relevantTweets.append(parsed_tweet)
    return relevantTweets

def exportData(query):
    tweets = getTweets(query)
    
    if len(tweets) == 0:
            sys.exit("Insufficient data.")
            
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
    # calling function to get tweets
    topics = []
    
    tweets = []
    posTweets = []
    negTweets = []
    neuTweets = []
    
    while 1:
        topic = input("Enter the topic to be analyzed (or 'quit' to stop): ")
        if topic == 'quit':
            break
        tweets = getTweets(topic)
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
        # percentage of nuetral tweets
        neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
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
        
        print("\n\nNeutral tweets:")
        for tweet in neutweets[:10]: 
            print(tweet['text']) 
            
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
        
if __name__ == "__main__": 
    # calling main function 
    main()
This method for Twitter Sentiment Analysis requires 4 steps:

1. Use getTweets.py with parameters for number of Twitter search pulls and seconds between pull.

2. Optionally use combineCSV.py to combine multiple CSV files for a larger graph.

3. Use tweetSentToCSV.py to analyze the sentiment of the Tweets (warning: potentially takes a very long time).

4. Run the Graph_Sentiment.ipynb Jupyter Notebook to graph the pre-analyzed CSV file.
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:48:13 2020

@author: CJ
"""
import pandas
import plotly.graph_objects as go

def sentGraph(filepath):
    data = pandas.read_csv(filepath)
    
    #data['time'] = pandas.DatetimeIndex(data.time)
    
    #data = data.set_index(['time'])
    '''
    times = pandas.DatetimeIndex(data.time)
    
    grouped = data.groupby(times.minute)['sentiment'].mean()
    '''
    
    fig = go.Figure(data=go.Scatter(x=data['time'],
                                    y=data['sentiment'],
                                    mode='markers',
                                    marker_color=data['sentiment'],
                                    text=data['text'],
                                    name='tweet'
                                    )) # hover text goes here
    
    avg_df = data.drop(['id', 'text'], axis=1)
    avg_df.time = pandas.to_datetime(avg_df.time)
    avg_df = avg_df.set_index('time').resample('T').mean()
    
    fig.add_trace(go.Scatter(x=avg_df.index,
                             y=avg_df.sentiment,
                             name='Avg Sentiment / 1Min',
                             line=dict(color='blue', width=2)
                             ))
    '''
    min_int = data.sentiment.resample('Min')
    fig.add_trace(x=min_int['time'], y=min_int['sentiment'])
    '''
    
    fig.update_layout(title='Coronavirus Twitter Sentiment Analysis')
    fig.show()

def main():
    filepath = input("Please input a file path: ")
    sentGraph(filepath)
    
if __name__ == "__main__": 
    # calling main function 
    main() 
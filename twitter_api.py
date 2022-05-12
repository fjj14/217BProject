from itertools import islice
from datetime import date, timedelta, datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import reverse_geocoder as rg
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

#gets 10 tweets per day within time range
def get_list(start_date, end_date, topic):
    temp = []
    prev = start_date
    for single_date in daterange(start_date, end_date):
        query = topic +" lang:en until:"+str(single_date) + " since:"+str(prev)
        prev = single_date
        currSet = sntwitter.TwitterSearchScraper(query).get_items()
        count = 0
        for curr in currSet:
            if count == 10:
                break
            else:
                temp.append(curr)
                count = count +1
    return temp


#the key is a number and the val is a list with [time period, start date, end date, topic]
all_queries = {
    1: [1, date(2012, 1, 1), date(2014, 12, 1), '"United States"'],
    2: [1, date(2012, 1, 1), date(2014, 12, 1), '"Barack Obama"'],
    3: [2, date(2015, 1, 1), date(2016, 10, 15), '"United States"'],
    4: [2, date(2015, 1, 1), date(2016, 10, 15), '"Barack Obama"'],
    5: [2, date(2015, 1, 1), date(2016, 10, 15), '"Donald Trump"'],
    6: [3, date(2017, 2, 1), date(2019, 12, 1), '"United States"'],
    7: [3, date(2017, 2, 1), date(2019, 12, 1), '"Donald Trump"'],
    8: [4, date(2020, 2, 1), date(2020, 10, 1), '"United States"' ],
    9: [4, date(2020, 2, 1), date(2020, 10, 1), '"Donald Trump"' ],
    10: [4, date(2020, 2, 1), date(2020, 10, 1), '"Joe Biden"' ],
    11: [5, date(2021, 2, 1), date(2022, 1, 1), '"United States"' ],
    12: [5, date(2021, 2, 1), date(2022, 1, 1), '"Joe Biden"' ],
    13: [6, date(2022, 2, 1), date(2022, 4, 21), '"United States"'],
    14: [6, date(2022, 2, 1), date(2022, 4, 21), '"Joe Biden"']
}

tweets = []

def fill_dataset():
  analyzer = SentimentIntensityAnalyzer()    
  for query, val in all_queries.items():
      currSet = get_list(all_queries[query][1], all_queries[query][2], all_queries[query][3])
      for tweet in currSet:
          if tweet.coordinates != None:
            lat = tweet.coordinates.latitude
            lon = tweet.coordinates.longitude
            coordinateInfo = rg.search((lat, lon), mode= 1)[0]
            country = coordinateInfo["cc"]
          else:
              country = "UNKNOWN"
          vs = analyzer.polarity_scores(str(tweet.content))
          tweets.append([tweet.date, tweet.content, country, all_queries[query][0], all_queries[query][3], vs])
  df = pd.DataFrame(tweets, columns=['Date', 'Content', 'Location', 'Period','Topic','Sentiment Scores'])
  df.to_csv("217BProject_data.csv")
  #sentiment_analysis_test(df)   # added in 

"""
Categorize tweets by country. Create Dictionary key: country, value: list of tuples, 
each tuple is time period and average score ex: US: [(1, .5), (3, -.2)]

"""
def analyze_dataset():
    df = pd.read_csv('217BProject_data.csv', lineterminator='\n')
    country_sentiment = {}
    for ind in df.index:
        country = df['Location'][ind]
        per = df['Period'][ind]
        curr = df['Sentiment Scores'][ind]
        curr_score = float(curr[curr.index("compound': ") + len("compound': "):-1])
        if country in country_sentiment:
            if per in country_sentiment[country]:
                count = country_sentiment[country][per][0]
                avg = country_sentiment[country][per][1]
                country_sentiment[country][per][0] = count + 1
                country_sentiment[country][per][1] = ((avg* count) + curr_score) / (count + 1)
            else:
                country_sentiment[country][per] = []
                country_sentiment[country][per].append(1)
                country_sentiment[country][per].append(curr_score)
        else:
            country_sentiment[country] = dict()
            country_sentiment[country][per] = []
            country_sentiment[country][per].append(1)
            country_sentiment[country][per].append(curr_score)
    multiple_entries = {}
    for key, val in country_sentiment.items():
        if len(country_sentiment[key]) > 1:
            multiple_entries[key] = val
    with open('Country_Results.csv', 'w') as f:
        for key in country_sentiment.keys():
            f.write("%s, %s\n" % (key, country_sentiment[key]))
    with open('Multiple_Entries.csv', 'w') as f:
        for key in multiple_entries.keys():
            f.write("%s, %s\n" % (key, multiple_entries[key]))

#fill_dataset()
analyze_dataset()

# steps to download to include in readme
# pip install vaderSentiment
# go into python terminal
# import nltk
# nltk.downloader.download('vader_lexicon')
#pip install reverse_geocoder




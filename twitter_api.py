from itertools import islice
from datetime import date, timedelta, datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import random
import numpy as np
#Todo Look at Sentiment

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
#gets 10 tweets per day within time range
def get_list(start_date, end_date, topic):
    temp = []
    prev = start_date
    for single_date in daterange(start_date, end_date):
        query = topic[0:len(topic)-1] +" lang:en until:"+str(single_date) + " since:"+str(prev)
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


#the key is the the query and the val is the time period of the six we chose that it falls in
all_queries = {
    '"United States"1': [1, date(2012, 1, 1), date(2014, 12, 1)],
    '"Barack Obama"2': [1, date(2012, 1, 1), date(2014, 12, 1)],
    '"United States3"': [2, date(2015, 1, 1), date(2016, 10, 15)],
    '"Barack Obama"4': [2, date(2015, 1, 1), date(2016, 10, 15)],
    '"Donald Trump"5': [2, date(2015, 1, 1), date(2016, 10, 15)],
    '"United States"6': [3, date(2017, 2, 1), date(2019, 12, 1)],
    '"Donald Trump"7': [3, date(2017, 2, 1), date(2019, 12, 1)],
    '"United States"8': [4, date(2020, 2, 1), date(2020, 10, 1)],
    '"Donald Trump"9': [4, date(2020, 2, 1), date(2020, 10, 1)],
    '"Joe Biden"0': [4, date(2020, 2, 1), date(2020, 10, 1)],
    '"United States"A': [5, date(2021, 2, 1), date(2022, 1, 1)],
    '"Joe Biden"B': [5, date(2021, 2, 1), date(2022, 1, 1)],
    '"United States"C': [6, date(2022, 2, 1), date(2022, 4, 21)],
    '"Joe Biden"D': [6, date(2022, 2, 1), date(2022, 4, 21)]
}

tweets = []
for query, val in all_queries.items():
    currSet = get_list(all_queries[query][1], all_queries[query][2], query)
    for tweet in currSet:
        tweets.append([tweet.date, tweet.content, tweet.user.location, all_queries[query][0]])
df = pd.DataFrame(tweets, columns=['Date', 'Content', 'Location', 'Period'])
df.to_csv("217BProject_data.csv")






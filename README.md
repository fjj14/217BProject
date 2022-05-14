# 217BProject
This project analyzes sentiment around the United States and relevant political figures within the last 10 years. 
We look at sentiment around six time periods and collect data from Twitter to analyze this sentiment.

twitter_api.py
 - scrapes data using snscrape and stores it in 217BProject_data.csv
   - stores date, location, time period, content, sentiment score
 - creates dictionaries storing averages of sentiment from a given country. This data is stored in Multiple_Entries.csv and Country_Results.csv. Country_results.csv stores all of the data collected. Multiple_Entries.csv contains data from countries that have entries from more than one time period.
   - key: country code where the tweet was posted from
   - val: dictionary
     - key: tuple(time period, topic)
     - val: list
       - index 0: number of tweets
       - index 1: average sentiment based on all of the tweets from the above time period AND topic


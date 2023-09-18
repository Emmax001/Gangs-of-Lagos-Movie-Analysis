# -*- coding: utf-8 -*-
"""
Created on Fri May 26 22:50:28 2023

@author: user
"""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import tweepy
from collections import Counter
import pandas as pd
from textblob import TextBlob
# Twitter API credentials
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Search query for tweets related to "Gangs of Lagos"
search_query = "Gangs of Lagos"

# Maximum number of tweets to scrape
max_tweets = 500

# Variables to store metrics
total_likes = 0
total_retweets = 0
total_tweets = 0
hashtags = []
sentiments = []

# List to store tweet details
tweet_details = []

# Initialize NLTK's SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Scrape tweets
tweets = tweepy.Cursor(api.search_tweets, q=search_query, lang="en", tweet_mode="extended").items(max_tweets)

# Process tweets and collect metrics
for tweet in tweets:
    # Extract relevant information from the tweet object
    total_likes += tweet.favorite_count
    total_retweets += tweet.retweet_count
    hashtags.extend([tag['text'] for tag in tweet.entities['hashtags']])
    
    # Perform sentiment analysis using NLTK's SentimentIntensityAnalyzer
    sentiment_scores = sid.polarity_scores(tweet.full_text)
    sentiment = sentiment_scores['compound']
    sentiments.append(sentiment)

    total_tweets += 1

   # Store the extracted data in a list
tweet_details.append({
    "Username": tweet.user.screen_name,
    "Tweet Text": tweet.full_text,
    "Likes": tweet.favorite_count,
    "Retweets": tweet.retweet_count,
    "Sentiment": sentiment,
    "Created At": tweet.created_at
})

# Create a DataFrame from the tweet details list
df = pd.DataFrame(tweet_details)

# Save the DataFrame to a CSV file
df.to_csv("gangs_of_lagos_analysis.csv", index=False)

# Calculate average daily tweets
average_daily_tweets = total_tweets / max_tweets

# Calculate popular hashtags
popular_hashtags = Counter(hashtags).most_common(5)

# Calculate Twitter sentiment
positive_sentiment = sentiments.count('positive')
negative_sentiment = sentiments.count('negative')
neutral_sentiment = sentiments.count('neutral')

# Calculate popular cast (assuming cast names are mentioned in tweets)
cast_mentions = ["Tobi Bakre", "Chike", "Chioma Akpotha", "Bimbo Ademoye", "Adesua Etomi", "Olarotimi Fakunle"]  # Replace with actual cast names
popular_cast = Counter(cast_mentions).most_common(4)

# Print the metrics
print(f"Total Likes: {total_likes}")
print(f"Total Retweets: {total_retweets}")
print(f"Average Daily Tweets: {average_daily_tweets}")
print(f"Total Tweets: {total_tweets}")
print(f"Popular Hashtags: {popular_hashtags}")
print(f"Twitter Sentiment: Positive={positive_sentiment}, Negative={negative_sentiment}, Neutral={neutral_sentiment}")
print(f"Popular Cast: {popular_cast}")

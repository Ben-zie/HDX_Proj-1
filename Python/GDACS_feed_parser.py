# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 19:28:29 2024

@author: Benjamin
"""

# Import package(s) for feeds parsing :
import feedparser

# Import packages for managing data :
import pandas as pd

#%% SET FEED CHANEL :

# Set source-feed-URL :
rss_url = "https://gdacs.org/xml/rss.xml"

# Here a list of other sources of feeds :
# CAUTION : every URL here is a todo item for each has to be checked as a data structure
#   rss_url = "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=3&format=raw"

# Parse URL :
feeds = feedparser.parse(rss_url)

feed_items = feeds["items"]


#%% KEY WORD SEARCH :

# This schunk may seem a bit verbose : it's vertue being to define a proper function for the word-search, 
# out of the 'apply' principle :

# Function to search for token in feeds title :
def search_in_title (feed_item, key_word = None) :
    """

    Parameters
    ----------
    feed_item : feedparser.util.FeedParserDict
        A single feed from a feeds pool from URL.

    Returns
    Boolean : for each feed, depending of the presence / absence of choosen word in the "title" item
    None.
    
    CAUTION : key word MUST not have majuscules in it
    """
    return(key_word in feed_item.title.lower())

# USAGE with apply :
# Transformation of feeds pool into a Dataframe :
df = pd.DataFrame(feed_items)
# Apply each line (item) of the pool with the function to get a mask:
# CAUTION : key word MUST not have majuscules in it
mask = df.apply(lambda x : search_in_title(x,key_word='argentina'),axis=1)
# Bracket selection using this mask for relevant feed to emerge :
title_select = df.loc[mask]

#%%

df.gdacs_eventtype.value_counts()

df.loc[df.gdacs_country.apply(lambda x : "France" in x)]


#%% SEARC FEEDS BY EVENT-TYPE :

# df.gdacs_eventtype.unique()
# -> array(['TC', 'FL', 'EQ', 'WF', 'DR'], dtype=object)
feed_size = len(feed_items)

for i in range(0,feed_size) : 
    print (feed_items[i].gdacs_eventtype)

df.loc[df.gdacs_eventtype == 'WF']

#%% SEARCH BY CRITERIAS :

# Select all feeds by 'alertlevel' to give impacted 'country'(s) :
event_filter = df.gdacs_alertlevel == 'Orange'
print("All countries concerned by this alert-level : \n", df.loc[event_filter].gdacs_country.unique())

# Control pannel :
event_type = 'EQ'
event_country = 'France'
event_alertlevel = 'Orange'
# Multi-criterial search :
event_filter_multi = (df["gdacs_alertlevel"] == 'Green') & (df["gdacs_eventtype"] == 'FL') & (df["gdacs_country"] == 'France')
df.loc[event_filter_multi]


# if needed, install HDX python library :
#    pip install hdx-python-api

import pandas as pd
import numpy as np
import pandas as pd

# Load package for regular expression management :
# https://docs.python.org/3/library/re.html
import re

# Load package for Humanitarian Data Exchange plateform connexion management :
from hdx.utilities.easy_logging import setup_logging
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

#%%
# SETUP MODULE

# Setup configuration for HDX client :
setup_logging()

# Setup configuration :
# Still in PROD server
Configuration.create(hdx_site="prod", user_agent="Myself_HDX-Proj_1", hdx_read_only=True)

#%%
# SEARCH MODULE

# Common search in HDX using client method :
datasets = Dataset.search_in_hdx("OCHA", rows=1000)
# More parameters avalilable by "get_*" methods of Dataset object :
# See https://github.com/Ben-zie/HDX_Proj-1/blob/main/Python_HDX-Proj-1.ipynb

# Stock "results" in a dataframe :
results = pd.DataFrame(datasets)

# results.info()
# results.shape

# Columns of 'results' are :
#       ['archived', 'batch', 'caveats', 'cod_level', 'creator_user_id',
#       'customviz', 'data_update_frequency', 'dataseries_name', 'dataset_date',
#       'dataset_preview', 'dataset_source', 'due_date', 'groups',
#       'has_geodata', 'has_quickcharts', 'has_showcases', 'id',
#       'is_requestdata_type', 'isopen', 'last_modified', 'license_id',
#       'license_other', 'license_title', 'license_url', 'maintainer',
#       'metadata_created', 'metadata_modified', 'methodology',
#       'methodology_other', 'name', 'notes', 'num_resources', 'num_tags',
#       'organization', 'overdue_date', 'owner_org', 'package_creator',
#       'pageviews_last_14_days', 'private', 'qa_checklist', 'qa_completed',
#       'relationships_as_object', 'relationships_as_subject', 'review_date',
#       'solr_additions', 'state', 'subnational', 'tags', 'title',
#       'total_res_downloads', 'type', 'updated_by_script', 'url', 'version']

#%%
# Lexical search in fields :
x = results[results[['cod_level']].notnull().all(1)]

results.sort_values(by = ['cod_level','dataset_date'],ascending=False)

# SOURCE : online python course on KAGGLE plateform :
def word_search(datasets_list, keyword):
    """
    Desc : function to search a (unique) KEYWORD in a field
    Input :  a LIST of textual documents (here NOTES categorie of a DATASET_LIST) + a KEYWORD to look after in each
    Output : a LIST of indexes of KEYWORD matching documents
    """
    # list to hold the indices of matching documents
    indices = [] 
    # Iterate through the indices (i) and elements (doc) of documents
    for i, dataset in enumerate(datasets_list):
        # Split the string doc into a list of words (according to whitespace)
        tokens = dataset.split()
        # Make a transformed list where we 'normalize' each word to facilitate matching.
        # Periods and commas are removed from the end of each word, and it's set to all lowercase.
        normalized = [token.rstrip('.,').lower() for token in tokens]
        # Is there a match? If so, update the list of matching indices.
        if keyword.lower() in normalized:
            indices.append(i)
    return indices

#%%
# searching for a WORD as 'token' in a field :

token = 'cod-ps'
field = 'name'

# Get the NAME field to choose dataset :
results.loc[results.name.apply(lambda x : token in x),field]

# Get the matching-dataset list :
results.loc[results.name.apply(lambda x : token in x),field]

#%%
# SORTING BY DATE MODULE

# Using package "re" for regular expressions :

# Set a function to get the dataset date from ['dataset_date'] (for datasets referenced by an intervall period, 
# the last one is chosen) and returned as a vector :
def get_date (x): 
    """
    Parameters : a dataframe containing research results from the HDX databse
    Returns : dates of different datasets in a vector object
    """
    x_dates = x.get('dataset_date')
    dates = []
    for i in x_dates : 
        dates.append(re.findall(r'(\d{4}-\d{2}-\d{2})(?!.*\d{4}-\d{2}-\d{2}T)', i))
    x['date_var'] = list(np.concatenate(dates).flat)
    x['date_var'] = pd.to_datetime(x['date_var'])
    return x

# Set a function to add a variable to dataset, containing date and sort dataset by this column :
def sort_by_date (x) :
    """
    Parameters : a dataframe containing research results from the HDX databse
    Returns : given dataset sorted by the last entry date in datas
    """
    x = get_date(x)
    x = x.sort_values(by='date_var',ascending=False)
    return x

#%%
# READ MODULE :

# Read dataset and get ressources :
dataset = Dataset.read_from_hdx("novel-coronavirus-2019-ncov-cases")
resources = dataset.get_resources()
for res in resources:
    url, path = res.download("C:/Users/Benjamin/Documents/UN/HDX/POOL")
    print(f"Resource URL {url} downloaded to {path}")

# Get infos on results :
# Results to dataframe
results = pd.DataFrame(dataset)
# See all "results" columns with dtypes :
results.dtypes
result.[....].describe()

# TODO : reshape types and variables : 
results["...."] = pd.Categorical(df["...."], ordered=....)
# Check dtypes :
# See all "results" columns with dtypes :
results.dtypes

# See all "results" columns :
results.columns
# See all "results" columns with dtypes :
results.dtypes
# Print specific field for all results (eg. "title")
results.loc[:,"title"]

#%%



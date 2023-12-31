# if needed, install HDX python library :
# pip install hdx-python-api

import pandas as pd
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Load package for REGULAR EXPRESSION management :
# https://docs.python.org/3/library/re.html
import re

# Load package for Humanitarian Data Exchange plateform connexion management :
from hdx.utilities.easy_logging import setup_logging
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

# SETUP MODULE
import HDX_proj_Python_Request

# Setup configuration for HDX client :
setup_logging()

# Setup configuration :
# Still in PROD server
Configuration.create(hdx_site="prod", user_agent="Myself_HDX-Proj_1", hdx_read_only=True)

# SEARCH MODULE
# Performs a research in HDX with existing Python client (see Wiki for more infos) :

#%%
# SORTING BY DATE MODULE

# Using package "re" for regular expressions :

# Set a function to get the dataset date from ['dataset_date'] (for datasets referenced by an intervall period, 
# the last one is chosen) and returned as a vector :
def set_date (x): 
    """
    Function : sets a DATE_BEFORE_VAR and a DATE_AFTER_VAR colums to dataset
    Those are date-formated : %Y-%m-%d
    Parameters : a dataframe containing research results from the HDX databse
    Returns : dates of different datasets in a vector object
    """
    # Import library

    # Extract column from results dataset :
    x_dates = results.get('dataset_date')
    # Get the pattern of each dates (FROM / TO) :
        # TODO : verify compatibility with database regarding from positionning in singles
    x_dates = x_dates.str.findall(r'(\d{4}-\d{2}-\d{2})T')
    # 'Serialize' the two columns :
    x_dates = x_dates.apply(lambda x : pd.Series(x))
    # Insert it in the original dataset :
    results['date_before_var'] = pd.to_datetime(x_dates[0],)
    results['date_after_var']  = pd.to_datetime(x_dates[1],)
    # Which we return :
    return x

# Set a function to add a variable to dataset, containing date and sort dataset by this column :
def sort_by_date (x, ascending=True, inplace = False) :
    """
    Function : Sorts a dataset by dates. Mainly a filter for 'select_by_date' function.
    Parameters : a dataframe containing research results from the HDX databse
    Returns : given dataset sorted by the last entry date in datas
    """
    # Call the 'set_date' function to have right columns to look in :
    x = set_date(x)
    # Use formated columns to sort dataset with :
    x = x.sort_values(by='date_before_var', ascending = ascending, inplace = inplace)
    return x

# Aggregated time-searching functions :
def select_by_date (results,
                    start_date,
                    end_date,
                    ascending = False,
                    inplace = False) :
    # From the 'results' dataset, set and sort the dates in formated columns :
    x = sort_by_date(results, ascending = ascending,inplace = inplace)
    # Cases for search FROM, TO or IN BETWEEN dates :
    if start_date != None and end_date != None :
        # Select DataFrame rows between two dates using DataFrame.isin()
        y = x[x["date_after_var"].isin(pd.date_range(start_date, end_date))]
        print('option 1 : find items in interval')
        # Source : https://sparkbyexamples.com/pandas/pandas-select-dataframe-rows-between-two-dates/
    elif start_date != None :
        # Selecting lower to the limit-date :
        mask = (x['date_after_var'] > start_date)
        y = x[mask]
        print('option 2 : find items upper the limit-date')
    elif end_date != None :
        # Selecting upper to the limit-date :
        mask = (x['date_after_var'] < end_date)
        y = x[mask]
        print('option 3 : find items lower the limit-date')
    else : 
        # No limit-date to search for
        print('no limits pointed for selection')
        y=None
    return y

# LEXICAL SERACH in fields :

# SOURCE : online python course on KAGGLE plateform :
def word_search(datasets_list, patern, field=None):
    """
    Desc : function to search a (unique) KEYWORD in a field
    Input :  a LIST of textual documents (here NOTES categorie of a DATASET_LIST) + a KEYWORD to look after in each
    Output : a LIST of indexes of KEYWORD matching documents
    """
    
    # list to hold the indices of matching documents
    indices = [] 
    datasets_list = datasets_list[field]
    # Iterate through the indices (i) and elements (doc) of documents
    for i, dataset in enumerate(datasets_list):
        # Split the string doc into a list of words (according to whitespace)
        tokens = dataset.split()
        # Make a transformed list where we 'normalize' each word to facilitate matching.
        # Periods and commas are removed from the end of each word, and it's set to all lowercase.
        normalized = [token.rstrip('.,').lower() for token in tokens]
        # Is there a match? If so, update the list of matching indices.
        if patern.lower() in normalized:
            indices.append(i)
    return indices

#%%
# Commande pannel :

# Defin Keyword(s) :
# Here an example KEYWORD for the research. Project being humanirarian oriented, the example involves COD datasets
# wich are crucial in any analysis.
# (Caution : space-separated if multiple words)
Keyword = "epidemic"
Keyword_infielf = 'ocha'
field = 'notes'
rows=1000

# Limit dates :
start_date = '2001-11-15'
end_date   = '2023-11-18'
ascending = True

# RESEARCH MODULE :

# 1.Common search in HDX using client method :
datasets = Dataset.search_in_hdx(Keyword, rows=rows)
# More parameters avalilable by "get_*" methods of Dataset object :
# See https://github.com/Ben-zie/HDX_Proj-1/blob/main/Python_HDX-Proj-1.ipynb

# 2.Store results in a dataframe :
results = pd.DataFrame(datasets)

# Columns in 'results' are :
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

#                      start_date=start_date,
#                      end_date=end_date,
#                      ascending=ascending,
#                      inplace=inplace

# results.info()
# results.shape

# 3.Run functions to apply time interval :
res = select_by_date(results = results,start_date=start_date,end_date=end_date,ascending=ascending)

# searching for a WORD as 'token' in a field :

# token = 'cod-ps'
# field = 'name'

# # Get the NAME field to choose dataset :
# results.loc[results.name.apply(lambda x : token in x),field]

# # Get the matching-dataset list :
# results.loc[results.name.apply(lambda x : token in x),field]

mask_word = word_search(res, patern = Keyword_infielf ,field = field)
# res = res.iloc[mask_word,:]
#%%

# READ MODULE :


# for i in range(1,len(res)) :
#     dataset_id = res.iloc[i].id
#     print(dataset_id)
#     path = os.path.join(parent_dir, dataset_id)
#     os.mkdir(path) 
#     # Read dataset and get ressources :
#     dataset = Dataset.read_from_hdx(dataset_id)
#     resources = dataset.get_resources()
#     for res in resources:
#         url, path = res.download(path)
#         print(f"Resource URL {url} downloaded to {path}")







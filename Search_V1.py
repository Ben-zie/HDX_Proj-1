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
datasets = Dataset.search_in_hdx("WHO", rows=1000)
# More parameters avalilable by "get_*" methods of Dataset object :
# See https://github.com/Ben-zie/HDX_Proj-1/blob/main/Python_HDX-Proj-1.ipynb

# Stock "results" in a dataframe :
results = pd.DataFrame(datasets)

# Search being completed, several variables are available in results, which are accessible 
# as columns of the "results dataframe" :
# archived                              bool
# batch                               object
# caveats                             object
# cod_level                           object
# creator_user_id                     object
# customviz                           object
# data_update_frequency               object
# dataseries_name                     object
# dataset_date                        object
# dataset_preview                     object
# dataset_source                      object
# due_date                            object
# groups                              object
# has_geodata                           bool
# has_quickcharts                       bool
# has_showcases                         bool
# id                                  object
# indicator                           object
# is_requestdata_type                   bool
# isopen                                bool
# last_modified                       object
# license_id                          object
# license_other                       object
# license_title                       object
# license_url                         object
# maintainer                          object
# metadata_created                    object
# metadata_modified                   object
# methodology                         object
# methodology_other                   object
# name                                object
# notes                               object
# num_resources                        int64
# num_tags                             int64
# organization                        object
# overdue_date                        object
# owner_org                           object
# package_creator                     object
# pageviews_last_14_days               int64
# private                               bool
# qa_checklist                        object
# qa_completed                          bool
# quality                             object
# relationships_as_object             object
# relationships_as_subject            object
# review_date                         object
# solr_additions                      object
# state                               object
# subnational                         object
# tags                                object
# title                               object
# total_res_downloads                  int64
# type                                object
# updated_by_script                   object
# url                                 object
# version                             object
# date_var                    datetime64[ns]


#%%
# SORT BY KEYWORD
def search_keyword (x, field = 'title', key = None) :
    """
    
    Parameters
    ----------
    x : dataframe
        original dataframe containing results of research on the HDX database.
    field : str, optional
        Filed in which look after the keyword ; default is 'title' (see above list of fields for more informations).
    key : str
        Keyword to look after ; default is None.

    Returns
    -------
    dat : dataframe
        List of items matching the research.
    """

    dat = x[x[field].str.contains(key, case = False)]
    return dat
#%%
# SORT BY DATE

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
def sort_by_date (x, low = None, up = None) :
    """
    Parameters : 
        x : a dataframe containing research results from the HDX databse
        low (optional) : lower year to select
        up (optional) : upper year to select
    Returns : given dataset sorted by the last entry date in datas
    """
    x = get_date(x)
    if low and up : 
        x = x[(x.date_var.dt.year > low) & (x.date_var.dt.year < up)]
    elif low :
        x = x[x.date_var.dt.year > low]
    elif up :
        x = x[x.date_var.dt.year < up]
    
    x = x.sort_values(by='date_var',ascending=False)
    return x

#%%
# SEARCH BY TYPE (geodata) :
def search_geodata (x, y) :
    """

    Parameters
    ----------
    x : dataframe (pandas)
        Source dataframe generated with results elements
    y : bool
        A boolean which tell if (Yes / No) you want to select elements corresponding to geodatas

    Returns
    -------
    x : dataframe
        Items found in HDX (from results passed in arguments) that correspond / dont correspond to geodatas.

    """
    x = x[x['has_geodata'] == y]
    return x

#%%
# SEARCH BY SOURCES :

def search_sources (x) :
    """

    Parameters
    ----------
    x : dataframe
        dataframe generated with reluts of a research in the HDX database.

    Returns
    -------
    tmp : list
        list of each sources presents in the results.

    """
    tmp = []
    pool_sources = x.dataset_source
    for i in pool_sources : tmp.append(re.findall(r'[^,]+(?=,|$)', i))
    tmp = list(np.concatenate(tmp))
    tmp = list(set(tmp))
    return tmp


def select_sources (x, y) :
    """

    Parameters
    ----------
    x : dataframe
        dataframe generatied with results of a research in the HDX database.
    y : str
        pattern to look for in the sources.

    Returns
    -------
    dataframe
        selection of items containing y in theire sources.

    """
    res = []
    for i in range(0,len(x)) :
        tmp = re.search(y, x.loc[i].dataset_source)
        if tmp :
            res.append(i)
    return x.loc[res]

#%%
# READ MODULE :
# Read dataset and get ressources :
dataset = Dataset.read_from_hdx('66829a94-1cc1-47fb-a5f3-fbd6cf3dbe26')
resources = dataset.get_resources()
for res in resources:
    url, path = res.download("C:/Users/Benjamin/Documents/UN/HDX/POOL")
    print(f"Resource URL {url} downloaded to {path}")

#%%
# CASE STUDY
dat = Dataset.search_in_hdx('palestine')
dat = pd.DataFrame(dat)
dat = search_geodata(dat, False)
sort_by_date(dat)[['title','dataset_date']]

#%%
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



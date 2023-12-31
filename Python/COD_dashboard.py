# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 00:18:19 2023

@author: Benjamin
"""
# if needed, install HDX python library :
# pip install hdx-python-api

import pandas as pd
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Load package for REGULAR EXPRESSION management :
# https://docs.python.org/3/library/re.html
# import re

# Load package for Humanitarian Data Exchange plateform connexion management :
from hdx.utilities.easy_logging import setup_logging
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

# SETUP MODULE
# from HDX_proj_Python_Request import *

# Setup configuration for HDX client :
setup_logging()

# Setup configuration :
# Still in PROD server
Configuration.create(hdx_site="prod", user_agent="Myself_HDX-Proj_1", hdx_read_only=True)

# SEARCH MODULE
# Performs a research in HDX with existing Python client (see Wiki for more infos) :

#%% Parametrization :

# Commande pannel :

# Defin Keyword(s) :
# Here an example KEYWORD for the research. Project being humanirarian oriented, the example involves COD datasets
# wich are crucial in any analysis.
# (Caution : space-separated if multiple words)
Keyword = "cod ps"
Keyword_infielf = 'ocha'
field = 'notes'
rows=1000

# Limit dates :
start_date = '2020-11-15'
end_date   = '2023-11-18'
ascending = True
inplace = False
# RESEARCH MODULE :

#%% Search in HDX using client method :

datasets = Dataset.search_in_hdx(Keyword, rows=rows)
# More parameters avalilable by "get_*" methods of Dataset object :
# See https://github.com/Ben-zie/HDX_Proj-1/blob/main/Python_HDX-Proj-1.ipynb

#%% Results to dataframe :

results = pd.DataFrame(datasets)

#%% Columns in 'results' :
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

#%% Run functions to apply time interval :

res = select_by_date(results = results,start_date=start_date,end_date=end_date,ascending=ascending)

results.info()
results.shape

#%% Word select :

mask_word = word_search(res, patern = Keyword_infielf ,field = field)
res_w = res.iloc[mask_word,:]

#%% Read dataset(s) :

dataset = Dataset.read_from_hdx(res.loc[2,:].id)

param_org = dict(dataset.get_organization())
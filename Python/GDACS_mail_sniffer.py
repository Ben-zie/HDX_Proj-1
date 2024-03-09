# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:44:34 2024

@author: Benjamin
"""
# Import packages :
#   Mesages manipulaiton :
# import email
from email import policy
from email.parser import BytesParser

#   others :
import os
import pandas as pd
import re
import glob

# Define path to messages pool and set in the working directory :
path = 'C:\\Users\\Benjamin\\Documents\\GITHub\\MailBase\\HDX_Proj_1-29_02_24'
os.chdir(path)
# List all ".eml" fils in the working directory :
file_list = glob.glob('*.eml')


# Open a single ".eml" file as a message :
# msg = BytesParser(policy=policy.default).parse(open(file_list[48],'rb'))

# Interesting methods applyable to messages :
    # see : https://docs.python.org/3/library/email.message.html
    # msg.items() # Messages being a dictionnary-like object, this method lists all couples : field-name / field-content
    # msg.__getitem__(name) # Method to get content of a particular field in messages
    # msg.keys() # Lists only fields-name in messages (gives access to message structure)

# NOTE THAT the text body of an email message is in the "_payload" item

# Method to get the textual body of a message :
# msg_text = msg.get_body(preferencelist='plain').get_content()

#%% OPEN MESSAGE :

def open_message(file_name) :
    """
    Parameters
    ----------
    file_name : string
        Name of an "*.eml".file

    Returns
    -------
    msg_text : string
        Text type body of the message.

    """
    # Open a single ".eml" file as a message :
    msg = BytesParser(policy=policy.default).parse(open(file_name,'rb'))
    
    # Interesting methods applyable to messages :
    # see : https://docs.python.org/3/library/email.message.html
    # msg.items() # Messages being a dictionnary-like object, this method lists all couples : field-name / field-content
    # msg.__getitem__(name) # Method to get content of a particular field in messages
    # msg.keys() # Lists only fields-name in messages (gives access to message structure)
    
    # NOTE THAT the text body of an email message is in the "_payload" item
    
    # Method to get the textual body of a message :
    msg_text = msg.get_body(preferencelist='plain').get_content()
    return msg_text

#%% GET EVENTS NUM :

# Get code for each event from their URL in message:
def get_event_num(msg_text) :
    """
    Parameters
    ----------
    msg_text : string
        Text type body of a mail (MUST come from GDACS).

    Returns
    -------
    msg_events : string
        Code of the event in the ....... nomenclature.

    """
    msg_events = re.findall(r'&eventid=(\d+)', msg_text)
    return msg_events

#%% GET MESSAGE PARAGRAPHES :
#------------------------------------------------------------------------------
# OLD :

# Get only usefull paragraphes regarding special symbols (={75}.....={70}) :
def get_event_paragraphes_all(msg_text):
    pattern = re.compile(r'={75}(.*?)={70}', re.DOTALL)
    msg_events_infos = pattern.findall(msg_text)
    return msg_events_infos

# TODO : eliminer les premiers et derniers paragraphes
#------------------------------------------------------------------------------

# Method to get each evenement related paragraphes :

def get_event_paragraphes(msg_text):
    """
    Parameters
    ----------
    msg_text : string
        Text type body of a GDACS newsletter mail.

    Returns
    -------
    paragraphes :list
        List containing every paragraphes about events (so begining with a alert color compatible word (['Green','Orange','Red']).

    """
    # Lists creation :
    select = list()
    event_id = list()
    # Select independently each paragraphe :
    paragraphes = re.split(r'\n\s*\n', msg_text)
    # Select every indices of paragraphes begging with an color-alert related word ['Green','Orange','Red'] AND with length supperior to 1 :
    for i in range(0,len(paragraphes)) :
        if len(paragraphes[i]) > 1 and paragraphes[i].split()[0] in ['Green','Orange','Red'] :
            select.append(i)
            event_id.append(re.findall(r'&eventid=(\d+)', paragraphes[i]))
    
    # Apply indices set as selection :
    paragraphes = list(paragraphes[i] for i in select)
    
    return paragraphes

#%% EARTHQUAKES :

def get_events_infos(paragraphe) :
    """
    Parameters
    ----------
    paragraphe : string
        Search paragraphs for infos on earthquake-like events :

    Returns
    -------
    date : double
        Event date, extracted from body-text.
    hour : time
        Event time, extracted from body-text.
    time : string
        Timal reference for event (eg. UTC).
    magnitude : Num
        Event magnitude, extracted from body text.
    Depth : Num
        Event Depth, extracted from body-text.
    """

    magnitude = re.findall(r'Magnitude\s*([^,\s]+)', paragraphe)
    if magnitude[0] == magnitude[1] :
        magnitude = magnitude[0]
    Depth = re.findall(r'Depth\:\s*([^\s]+\s*km)', paragraphe)
    if Depth[0] == Depth[1] :
        Depth = Depth[0]
    date_hour = re.findall(r'\b\d{2}/\d{2}/\d{2}.*?UTC\b', paragraphe)
    date, hour, time = re.split(' ',date_hour[0])

    return date, hour, time, magnitude, Depth

#%%

def main(msg_text) :
    """
    Parameters
    ----------
    msg_text : string
        Text type mail body.

    Returns
    -------
    df : pd.Dataframe
        Dataframe each line containing infos for an earthquake ; columns = ['Date','Heure','Fuseau_h','Magnitude','Profondeur'].

    """
    magnitudes = list()
    Depths = list()
    dates = list()
    hours = list()
    times = list()

    paragraphes = get_event_paragraphes(msg_text)
    
    for par in paragraphes :
        if 'earthquake' in par :
            date, hour, time, magnitude, Depth = get_events_infos(par)
            magnitude = magnitude.strip("M")
            Depth = Depth.strip('km')
            dates.append(date)
            hours.append(hour)
            times.append(time)
            magnitudes.append(magnitude)
            Depths.append(Depth)
    df = pd.DataFrame(list(zip(dates, hours, times, magnitudes, Depths)))
    df.loc[:,3] = pd.to_numeric(df.loc[:,3])
    df.loc[:,4] = pd.to_numeric(df.loc[:,4])
    return df

#%% CONTROL PANEL :

Seismes = pd.DataFrame()

for f in file_list[0:50] :
    msg_text = open_message(f)
    if len(msg_text)>0 :
        df = main(msg_text)
        Seismes = pd.concat((Seismes,df))

Seismes.columns = ['Date','Heure','Fuseau_h','Magnitude','Profondeur (Km)']

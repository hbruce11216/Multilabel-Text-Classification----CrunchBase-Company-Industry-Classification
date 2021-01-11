#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:35:05 2021

@author: holdenbruce
"""


# Maybe the way to generalize the approach of increasing the training dataset
# is to loop through the list of CB given industries and determine if any
# of those match words from the CB_Description column for that company.
# If there is a direct match then we should be pretty confident that we 
# have correctly identified the industry

# (1) In this python file I am going to start by loading the entire 50k dataset
# (2) Then I will parse the CB_Industries column so that it is a list of terms
# (3) Then I will loop through each company's list of CB_Industries and see if
#     there is a direct match of any of the industry classifications to words
#     found in the CB_Descriptions column   
# (4) Now I will hopefully have a large enough training set to train an NLP model
# (5) If I do not (if the NLP model still performs poorly) then I will move 
#     away from my current approach and figure out how to string together a 
#     series of logical checks to determine confidence in my classifications...
#     taking the elements of what I have already produced in trying to build out
#     my training set and repurposing it 

# (6) Another interesting idea I have is to have a dictionary of Industry Keywords
#     that gets looped through and each keyword is checked if it is in that 
#     company's CB Description. We get more confident with the classification if
#     there are more than like 2 matches.

# (7) Ideally, the company descriptions are longer. It would be great to have 
#     longer descriptions so sentiment could actually be analyzed. 



# (1) In this python file I am going to start by loading the entire 50k dataset
import pandas as pd
#load full database excel
df = pd.read_excel('IndustryClassificationData.xlsx')
df.head()
df.shape #the entire IndustryClassificationData.xlsx contains 46,458 companies
#get rid of all companies that have nulls in the CB Industries column
df = df[pd.notnull(df['CB Industries'])].reset_index(drop=True)
df.shape #(45979, 7)...after getting rid of companies with blank 'CB Industries'
#columns, we are left with 45,979 companies, dropping 479 companies



# (2) Then I will parse the CB_Industries column so that it is a list of terms

# for loop to extract companies that have less than 2 industries assigned
# to their CB Industries column:
def split_cb_industries(dataframe):

    counter = 0
    industry_split = []
    #loop through each company in the CB Industries column
    for industry in dataframe['CB Industries']:
        #turn company to string
        industry = str(industry)
        #if there are only one listed industry for the company
        
        #use regex to split on both ',' and ';'
        import re
        split_inds = re.split('; |,', industry)
        
        if split_inds[0]!='nan':
            industry_split.append(split_inds)
            
        #just using a counter because i'm curious, can be removed
        if len(split_inds) > 2:
            counter+=1
    
    # industry_split = [x.strip(' ', '') for x in industry_split]
    
    for company_index in range(len(industry_split)):
        for industry_phrase in range(len(industry_split[company_index])):
            industry_split[company_index][industry_phrase] = industry_split[company_index][industry_phrase].strip()

    

    return industry_split, counter
    
    
df_industry_split, num_counter = split_cb_industries(df)
#df_train_ind_sub_2 is a string of all the industries
#df_train_ind_sub_2 is a list of all the industries

# Now assign the df_industry_split to the df['CB Industries']
df['CB Industries'] = df_industry_split
df['CB Industries'].str.split()









# (3) Then I will loop through each company's list of CB_Industries and see if
#     there is a direct match of any of the industry classifications to words
#     found in the CB_Descriptions column   

industry_taxonomy = pd.read_csv('IndustryTaxonomy.csv', header=None)
industry_taxonomy.columns = ['Industry']


# Let's start by reducing the 87 industries and instead do a matching
# to see how that performs.
# How to replace an entire column with something 
# https://kanoki.org/2019/07/17/pandas-how-to-replace-values-based-on-conditions/

# Automotive
# Automotive Services
industry_taxonomy[(industry_taxonomy['Industry']=='Automotive Services')] = 'Automotive'
# SAAS - Automotive
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Automotive')] = 'Automotive'


#Financial Services & Accounting
# Banking
industry_taxonomy[(industry_taxonomy['Industry']=='Banking')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Private Equity')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Venture Capital')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Finance/HR - Accounting')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Finance/HR - Payroll')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Finance/HR - Recruiting')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Payroll')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Point of Sale')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Point of Sale')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Accounting')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Payments')] = 'Financial Services & Accounting'
industry_taxonomy[(industry_taxonomy['Industry']=='Financial Service')] = 'Financial Services & Accounting'


#Human Resources
# SAAS - Finance/HR - ERP
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Finance/HR - ERP')] = 'Human Resources'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Finance/HR - Human Resources')] = 'Human Resources'
industry_taxonomy[(industry_taxonomy['Industry']=='E-Signature')] = 'Human Resources'
industry_taxonomy[(industry_taxonomy['Industry']=='Enterprise Resource Planning (ERP)')] = 'Human Resources'


#Energy
# Carbon Measurement & Mgmt
industry_taxonomy[(industry_taxonomy['Industry']=='Carbon Measurement & Mgmt')] = 'Energy'
industry_taxonomy[(industry_taxonomy['Industry']=='Carbon Measurement & Mgmt')] = 'Energy'


#Computer Hardware
# Tech - Hardware
industry_taxonomy[(industry_taxonomy['Industry']=='Tech - Hardware')] = 'Computer Hardware'


#Computer Software (broad)
# Software
industry_taxonomy[(industry_taxonomy['Industry']=='Software')] = 'Computer Software'



#Consulting / Market Research
industry_taxonomy[(industry_taxonomy['Industry']=='Consulting')] = 'Consulting & Market Research'
industry_taxonomy[(industry_taxonomy['Industry']=='Market Research')] = 'Consulting & Market Research'


#Education
industry_taxonomy[(industry_taxonomy['Industry']=='E-learning')] = 'Education'
industry_taxonomy[(industry_taxonomy['Industry']=='Education Management')] = 'Education'
industry_taxonomy[(industry_taxonomy['Industry']=='Educational')] = 'Education'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - EdTech')] = 'Education'
industry_taxonomy[(industry_taxonomy['Industry']=='EdTech')] = 'Education'



#Food Services / Grocery
industry_taxonomy[(industry_taxonomy['Industry']=='Food Services')] = 'Food Services & Grocery'
industry_taxonomy[(industry_taxonomy['Industry']=='Grocery')] = 'Food Services & Grocery'



#Health, Wellness & Fitness
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Fitness')] = 'Health, Wellness & Fitness'


# Hospital & Health Care / Medical Device
industry_taxonomy[(industry_taxonomy['Industry']=='Hospital & Health Care')] = 'Hospital, Health Care & Medical Device'
industry_taxonomy[(industry_taxonomy['Industry']=='Medical Device')] = 'Hospital, Health Care & Medical Device'



#Hotels & Resorts / Hospitality
industry_taxonomy[(industry_taxonomy['Industry']=='Hotels & Resorts')] = 'Hotels & Resorts & Hospitality'
industry_taxonomy[(industry_taxonomy['Industry']=='Hotels and Resorts')] = 'Hotels & Resorts & Hospitality'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Hospitality')] = 'Hotels & Resorts & Hospitality'



#Information Services
industry_taxonomy[(industry_taxonomy['Industry']=='Information Technology & Services')] = 'Information Services'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Services Management')] = 'Information Services'


# Logistics & Supply Chain
industry_taxonomy[(industry_taxonomy['Industry']=='Shipping')] = 'Logistics & Supply Chain'


#Manufacturing 
industry_taxonomy[(industry_taxonomy['Industry']=='Industrial Automation')] = 'Manufacturing'


#Marketing
industry_taxonomy[(industry_taxonomy['Industry']=='Marketing & Advertising')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='Performance Marketing Agency')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Marketing Tech - Demand Generation')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Marketing Tech - Email Marketing')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Marketing Tech - Marketing Automation')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Marketing Tech - SEO')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='Email Marketing')] = 'Marketing'
industry_taxonomy[(industry_taxonomy['Industry']=='Marketing Automation')] = 'Marketing'


#Publishing
industry_taxonomy[(industry_taxonomy['Industry']=='Publication Tool')] = 'Publishing'
industry_taxonomy[(industry_taxonomy['Industry']=='Publishing - Traditional')] = 'Publishing'
industry_taxonomy[(industry_taxonomy['Industry']=='Educational Publishing')] = 'Publishing'


#Retail
industry_taxonomy[(industry_taxonomy['Industry']=='Retail - eCommerce')] = 'Retail'
industry_taxonomy[(industry_taxonomy['Industry']=='Retail - Box Store')] = 'Retail'


#Sales & Customer Service
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - CRM')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Customer Service')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Feedback')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Sales - AI/Sales Intelligence')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Sales - CRM')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Sales - eSignature')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='Sales Automation')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='Customer Service')] = 'Sales & Customer Service'
industry_taxonomy[(industry_taxonomy['Industry']=='CRM')] = 'Sales & Customer Service'


#Staffing 
industry_taxonomy[(industry_taxonomy['Industry']=='Staffing')] = 'Staffing & Recruiting'
industry_taxonomy[(industry_taxonomy['Industry']=='Recruiting')] = 'Staffing & Recruiting'


#Internet - misc.
industry_taxonomy[(industry_taxonomy['Industry']=='Internet')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='Tech - Internet - C2C Marketplace')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='Tech - Internet - Gig Economy')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Travel Management')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Contractor Engagement')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - eCommerce')] = 'Internet Marketplace - misc.'
industry_taxonomy[(industry_taxonomy['Industry']=='E-Commerce Platforms')] = 'Internet Marketplace - misc.'


# Social Media & Social Networks
industry_taxonomy[(industry_taxonomy['Industry']=='Tech - Internet - Social Networks')] = 'Social Media & Social Networks'
industry_taxonomy[(industry_taxonomy['Industry']=='Social Media')] = 'Social Media & Social Networks'
industry_taxonomy[(industry_taxonomy['Industry']=='Social Networks / Social Media')] = 'Social Media & Social Networks'
 

# Trade Show / Event Management
industry_taxonomy[(industry_taxonomy['Industry']=='Trade Show Organizers')] = 'Trade Show & Event Management'
industry_taxonomy[(industry_taxonomy['Industry']=='SAAS - Marketing Tech - Event Management')] = 'Trade Show & Event Management'
industry_taxonomy[(industry_taxonomy['Industry']=='Event Management')] = 'Trade Show & Event Management'


# Now use drop_duplicates() to drop the duplicates and reset_index() to reset the index
industry_taxonomy = industry_taxonomy['Industry'].drop_duplicates().reset_index(drop=True)
# There are 38 industries, down from 87










# First I will create the 

# maybe i could shrink the industry_taxonomy down
# and then manually find keywords for the industries that remain 







df['CB Industries'][0]

for company_index in range(len(df['CB Industries'][0:10])):
    counter = 0
    #looks at each keyword phrase in the CB Industries column
    for phrase in df['CB Industries'][company_index]:
        #prints when there is a match where the keyword phrase is found in the CB Description 
        if phrase.lower() in df['CB Description'][company_index].lower():
            counter += 1
            print(df['CB Industries'][company_index], '...', phrase, '...', df['CB Description'][company_index])
    print(counter)
    
    for word in df['CB Description'][0].split():
        for industry in industry_taxonomy:
            if word in industry.lower():
                print(word)
    
    
df['industry'] = 







#we are focusing on the descriptions column to predict the industry
col = ['CB Description', 'CB Industries']
df_pred = df[col]
df_pred.columns
df_pred['industry'].unique()

## I MIGHT NEED THIS STUFF: 
#add column names 
df_pred.columns = ['CB_Description', 'industry']
df_industry_factorized = df_pred.loc[:,'industry'].factorize()[0]
df_pred['industry_id'] = df_industry_factorized 
df_pred  #there are 66 different labels in our training group

# this saves the unique industires down to a variable 'industry_id_df'
from io import StringIO
industry_id_df = df_pred[['industry', 'industry_id']].drop_duplicates().sort_values('industry_id').reset_index(drop=True)
industry_id_df 
industry_to_id = dict(industry_id_df.values)
id_to_industry = dict(industry_id_df[['industry_id', 'industry']].values)
df_pred.head()






# this little snippet of code looks at each description and industry title and
# sees if the current industry classification has one of the words (utilities, 
# social, etc) in the description
# if it does, it returns the word, the key, and the description
# from there, i can look at which descriptions are returned 


matches = []
# for description in df_train_reduced_fewer_industries['CB_Description'].head():
# for description in range(len(df_train_reduced_fewer_industries)):
for description in range(5):
    # print(description,'\n')
    # matches_per_key = []
    for key in range(len(id_to_category)):
        # print(id_to_category[key],'\n')
        industry = str(id_to_category[key].lower())
                
        keys = industry.split()
        # print(keys)
        keys = [w for w in keys if w != '&' and 'service' not in w] #get rid of "&" and 'service'
        # print(keys)
        
        for word in keys:
            # print(word)
            # if word in description:
            if word in df_train_reduced_fewer_industries['CB_Description'][description]:
                # print(word, key, description)
                # matches_per_key.append([word,key,description])
                # matches.append([word,key,description])
                # matches.append([word,':',key,',',df_train_reduced_fewer_industries['CB_Description'][description],':',description])
                matches.append([word,key,df_train_reduced_fewer_industries['CB_Description'][description],description])
                # print(matches_per_key)
                #index 0 contains the word from the industry classification that was matched with the cb_description
                #index 1 is the key index for the industry dictionary
                #index 2 is the cb_description 
                #index 3 is the company id 
# df_train_reduced_fewer_industries.loc[9816] 
len(matches)
for match in matches:
    print(match)

#this creates a dictionary of matches
#where each key is the company id
#and the corresponding value is the entire entry (4 indices) from the matches list
matches_dict = {}
for match in matches:
    company_id = match[-1]
    if company_id not in matches_dict:
        matches_dict[company_id] = [match[:]]
    else:
        matches_dict[company_id] += [match[:]]
matches_dict[2]


#this looks within the dictionary to find keys that have more than one value
#these instances need to be compared and assigned some value
#do we combine them together to see if the entire phrase is in the cb_description?
#if we only look at the individual keywords, which do we prioritize?
#which industry keyword do we weight more? 

#this keeps track of how many descriptions were updated from exact matches in
#joining the different parts / from the entire industry phrase being present
#in the cb_descriptions
counter_of_how_many_cb_descriptions_were_updated = 0

#here, 'match' is the key from the matches_dict
#that key corresponds to the company id stored in index 3 of the matches list
for key in matches_dict:
    print(matches_dict[key])
    # print(match)
    if len(matches_dict[key]) > 1:
        print(matches_dict[key])
        entire_phrase = ''
        for match in matches_dict[key]:
            print(match)
            entire_phrase += '{} '.format(match[0])
        #using :-1 to chop off the trailing space 
        entire_phrase = entire_phrase[:-1]
        
        
        #now check if that entire phrase is in the description, which is in index [0][2]
        #if it is, then just go ahead and rewrite the CB_Description in df_train_reduced_fewer_industries 
        #so that it that industry classification 
        if entire_phrase in matches_dict[key][0][2]:
            df_train_reduced_fewer_industries['CB_Description'][matches_dict[key][0][-1]] = id_to_category[matches_dict[key][0][1]]
            counter_of_how_many_cb_descriptions_were_updated += 1
        # elif 
            
            
df_train_reduced_fewer_industries['CB_Description'][2]  
id_to_category[matches_dict[match][0][1]]

matches_dict[0][0][2]












# (6) Another interesting idea I have is to have a dictionary of Industry Keywords
#     that gets looped through and each keyword is checked if it is in that 
#     company's CB Description. We get more confident with the classification if
#     there are more than like 2 matches.

# I will use the contents from this link to create a dictionary
# https://www.labor.ny.gov/agencyinfo/industrykeywords.shtm






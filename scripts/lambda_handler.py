
import json 
import boto3
import os
import numpy as np
from sqlalchemy import create_engine
import pandas as pd

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']


connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string, echo=True)
connection = engine.connect()
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket_name = 'accredited-online-colleges-in-us'
    key = 'school_data.json'
    
    print(bucket_name)
    print(key)        

    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = response['Body'].read().decode('utf-8')
    json_obj = json.loads(file_content)
    
    
    school_df = pd.DataFrame(json_obj)
    
    school_df.columns = school_df.columns.str.lower().str.replace(' ', '_')
    school_df.rename(columns={'school': 'school_name', 'tuition_and_fees': 'tuition',
                          'region':'state', 'school_type':'school_info'}, inplace=True)
    school_df['tuition'] = school_df['tuition'].str.replace('$', '')
    school_df['tuition'] = school_df['tuition'].str.replace(',', '')
    school_df['tuition'] = school_df['tuition'].replace('N/A', np.nan)
    school_df['tuition'].dropna(inplace=True)
    school_df['tuition'] = school_df['tuition'].astype('Int64')
    

    # split column into multiple columns, to account for multiple entries
    degree_levels = school_df['degree_level'].str.split(', ', expand=True)
    degree_levels.columns = [f"degree_{i+1}" for i in range(degree_levels.shape[1])]
    school_df = pd.concat([school_df, degree_levels], axis=1)
    school_df.drop('degree_level', axis=1, inplace=True)

    school_info_split = school_df['school_info'].str.split(', ', expand=True)
    school_info_split.columns = ['school_type', 'duration']
    school_df = pd.concat([school_df, school_info_split], axis=1)
    school_df.drop('school_info', axis=1, inplace=True)
    
    print(school_df.columns)

    
    
    

    # dictionary to map state name to state appreviations
    us_state_abbreviations = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }

    school_df['state'] = school_df['state'].replace(us_state_abbreviations)

    school_df.to_sql("us_accredited_online_colleges", connection, if_exists='append', index=False)
    
    connection.close()
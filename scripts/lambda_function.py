
import json 
import pandas as pd
import boto3
from sqlalchemy import create_engine
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DB_HOST = config['database']['host']
DB_USER = config['database']['user']
DB_PASSWORD = config['database']['password']
DB_NAME = config['database']['database']



connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string, echo=True)
connection = engine.connect()


def lambda_handler(event, context):
    
    bucket_name = 'accredited-online-colleges-in-us'
    key = 'school_data.json'
    
    s3 = boto3.resource('s3')

    content_object = s3.Object(bucket_name, key)
    file_content = content_object.get()['Body'].read().decode('utf-8')
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
    
if __name__ == '__main__':
    lambda_handler(None, None)
        

# lambda function to convert reference_data from JSON to Parquet
import pandas as pd
import awswrangler as wr
import urllib.parse
import os
#env variables
s3_cleansed_layer = os.environ['s3_cleansed_layer']
glue_catalog_db = os.environ['glue_catalog_db']
glue_catalog_table = os.environ['glue_catalog_table']

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name'
    ]
    # we use urllib methods for replacing url string characters into their corresponding values
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],encoding='utf-8')
     
    #creating df
    df_raw = wr.s3.read_json('s3://{}/{}'.format(bucket,key))
    
    
    #extract required columns from "items" key
    df_raw = pd.json_normalize(df_raw['items'])
    
    
    #write clean data back to S3 and update Glue data catalog
    res = wr.s3.to_parquet(
        df=df_raw,
        path=s3_cleansed_layer,
        dataset=True ,
        database=glue_catalog_db,
        table=glue_catalog_table,
        
        )
    return res
    
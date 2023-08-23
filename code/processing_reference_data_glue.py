# notebook for json to parquet in Glue
# this also includes flattening JSON items

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

s3_path = "s3://data-analysis-project123/raw/reference_data/"

df_ref_data= glueContext.create_dynamic_frame_from_options(connection_type= 's3',
                connection_options={"paths": [s3_path]}, format='json')

df_ref_data.toDF().show()

# select "items" columns for creating rows
exploded_df = df_ref_data.select_fields(["items"])
exploded_df.toDF().show()


df_list = exploded_df.relationalize('root',"s3://data-analysis-project123/raw/")

print(df_list.keys())

df_list.select("root_items").toDF().show()

df_unnested = df_list.select("root_items").drop_fields(['id','index'])
print(df_unnested.count())

S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
                    frame=df_unnested, connection_type="s3",
                    format="glueparquet",
                    connection_options={"path": "s3://et1-glue-cleansed-data-analysis-project123/reference_data/",
                                        "partitionKeys": [],
                    },
                    format_options={"compression": "snappy"}
)

job.commit()

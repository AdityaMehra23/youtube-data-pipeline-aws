# script to join reference_data and statistics table and create a reporting layer 
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


# read data from AWS Glue Data Catalog-reference
AWSGlueDataCatalogreference_node1692797931989 = (
    glueContext.create_dynamic_frame.from_catalog(
        database="cleansed-youtube-data",
        table_name="reference_data_cleansed",
        transformation_ctx="AWSGlueDataCatalogreference_node1692797931989",
    )
)

# read data from AWS Glue Data Catalog-statistics. Use push_down_predicate for region to avoid reading regions with unparseable data
AWSGlueDataCatalogstatistics_node1692797911444 = (
    glueContext.create_dynamic_frame.from_catalog(
        database="raw-youtube-data",
        table_name="statistics",
        transformation_ctx="AWSGlueDataCatalogstatistics_node1692797911444",
        push_down_predicate="region='ca'"
    )
)

#  Join the two dynamic frame
Join_node1692797991123 = Join.apply(
    frame1=AWSGlueDataCatalogstatistics_node1692797911444,
    frame2=AWSGlueDataCatalogreference_node1692797931989,
    keys1=["category_id"],
    keys2=["id"],
    transformation_ctx="Join_node1692797991123",
)

# Here we can filter out any records by region
Filter_node1692798798802 = Filter.apply(
    frame=Join_node1692797991123,
    f=lambda row: (bool(re.match("^(?!us)", row["region"]))),
    transformation_ctx="Filter_node1692798798802",
)

# Load data to Amazon S3
AmazonS3_node1692798031148 = glueContext.getSink(
    path="s3://data-analysis-project-reporting",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=["region", "category_id"],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1692798031148",
)
# update AWS Glue table
AmazonS3_node1692798031148.setCatalogInfo(
    catalogDatabase="reporting-db", catalogTableName="video-likes"
)
AmazonS3_node1692798031148.setFormat("glueparquet")
AmazonS3_node1692798031148.writeFrame(Filter_node1692798798802)


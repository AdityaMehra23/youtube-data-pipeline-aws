# youtube-data-pipeline-aws

The main objective of this project is to leverage YouTube video statistics, including likes, views, and comments, to gain comprehensive insights into the behavior and preferences of the target audience.

## Data Source
https://www.kaggle.com/datasets/datasnaek/youtube-new

## Description
The ETL data pipeline used S3 buckets as the primary data source and storage repository. The data was initially processed using S3 triggers and Lambda. The same was also implemented using Glue Studio (Spark-based jobs). The cleansed data was stored in AWS data catalog for in-depth analysis using AWS Athena. S3 Lifecycle policies were used to remove outdated data. A reporting layer was built on top of existing tables for faster querying. Finally, AWS QuickSight was used to visualize the data in the form of charts and graphs.

## Use-cases
1. Audience Segmentation: To analyze the video statistics to segment the audience based on factors such as age, gender, location, and interests. This information can help tailor marketing campaigns and content to specific audience segments.
2. Trend Identification: Monitor trends in video engagement over time. To identify which types of videos are consistently popular, allowing us to create content that aligns with these trends. 
3. Ad Campaign Effectiveness: To analyze the correlation between advertisement campaigns and changes in engagement metrics. Measure how the campaigns impact views, likes, and comments.

## Steps
1. Load the reference_data (JSON) and statistics (CSV) to S3 buckets.
2. Create AWS Glue Crawlers to read objects from S3. Proper IAM role needs to be created.
3. Set up AWS Athena to read data from AWS Data Catalog.
4. Create Lambda function to convert JSON to Parquet. It will be triggered by S3 triggers.
![](/img/json-parquet-lambda-s3-trigger.png)
5. Write spark-based job in AWS Glue Jupyter notebook. It requires appropriate IAM role and policies.
![](/img/json-parquet-glue.png)
6. Converting datatypes of columns in Glue tables can be done by changing schema in AWS Data Catalog and then reloading the tables from S3. It can be implemented using Lambda and Glue Jobs.
![](/img/json-parquet-lambda-s3-trigger-schema-update.png)
![](/img/json-parquet-glue-schema-update.png)
7. Create Glue job to convert statistics data from CSV to Parquet. 
8. Create a reporting layer by joining processed reference_data and processed statistics data using Glue. The spark script can be modified for specific purposes such as adding push_down_predicate option to read specific partitions.
![](/img/reporting-layer-glue.png)
8. Now query table in the reporting layer using Athena.
![](/img/reporting-layer-athena.png)
9. Create reporting layer table in Athena as QuickSight data source. Now below graphs can be visualized.
Number of likes per video, filtered by videos having likes greater than 1 M.
![](/img/data-vis-1.png)
We can compare that with the channels that received maximum views.
![](/img/data-vis-2.png)
An interesting trend is observed when views for Education and Gaming videos are plotted over time.
![](/img/data-vis-3.png)
A better picture of total views can be observed using pie-chart
![](/img/data-vis-4.png)
We can also filter create same chart with other categories to visualize the views.
![](/img/data-vis-5.png)
By incorporating more specific data, such as the time of day, we can pinpoint when different users are most active. Geo Maps can be made to identify regions where certain videos are particularly popular. Furthermore, we can determine the Top-N most liked or disliked videos within a given category.




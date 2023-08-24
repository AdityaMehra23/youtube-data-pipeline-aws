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

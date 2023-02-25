# Twitter ETL Pipeline

Development of automated data pipelines to extract twitter data, with a sentiment analysis

---

## Table of contents

-   [Tech stack](https://github.com/Dorad-H/Twitter-ETL-Pipeline#tech-stack)
-   [ETL pipleline](https://github.com/Dorad-H/Twitter-ETL-Pipeline#extract-transform--load)
-   [ELT pipeline](https://github.com/Dorad-H/Twitter-ETL-Pipeline#extract-load--transform)
-   [Machine Learning](https://github.com/Dorad-H/Twitter-ETL-Pipeline#machine-learning)
-   [Authors](https://github.com/Dorad-H/Twitter-ETL-Pipeline#authors)

---

## Description

Social media platforms have become a valuable source of data for various industries, including marketing, research, and public opinion analysis. Twitter, in particular, is a popular platform for real-time information exchange and communication, making it a valuable source of data for businesses and researchers alike. However, extracting and analyzing data from Twitter can be challenging due to the sheer volume and unstructured nature of the data. This is where an ETL (Extract, Transform, Load) pipeline comes in handy.

The goal of this project is to develop an ETL pipeline that extracts Twitter data, specifically tweets and replies to those tweets, and stores them in a relational database. The pipeline will perform various transformations on the data to ensure that it is clean, consistent, and ready for analysis.

## Tech stack

-   #### Python

    Used to create the extract and transform the twitter data.

-   #### Apache Airflow

    Used to Automate and monitor the pipeline.

-   #### PostgreSQL
    A relational database Used to store the transformed data.

## Extract, Transform & Load

Used for structured data, transformed within python to conform to the below model to ensure the database remained efficient and sacable in future.
![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/f2fb2f6d67c421ec0cf907aef06637455465ecac/ER%20diagram.png "ER Diagram")

## Extract, Load & Transform

Used for semi-structured data, relevant variables extracted in JSON format. Stored in the database in the below format which could then be extracted and transformed for needed use.
![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/917c0e72d1e1e96f7d7d9f3a6674ee1d35b355e6/Semi%20structured.png "JSON format")

## Machine Learning

Sentiment analysis of company tweets using the [VADER package.](https://github.com/cjhutto/vaderSentiment) Sentiment of tweets scored using this package -1 to 1 with the following groupings shown below:

-   Negative
-   Neutral (-0.05 to 0.05)
-   Positive

Logistic Regression used to predict the sentiments by a company

-   Accuracy of 72%
-   F1 score of 0.75 on positive values

# Authors

-   [Dorad Hasani](https://studentsunionucl.org/sites/default/files/u198411/image00060.jpeg)
-   [Jan Salcedo](https://github.com/SuperSalcedo22)
-   [Pernelle Gamrowski](https://github.com/pernelleg)
-   [Helen Luhaäär](https://github.com/HelenLB)

[Back to the top](https://github.com/Dorad-H/Twitter-ETL-Pipeline#twitter_pipeline)

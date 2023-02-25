# Twitter ETL Pipeline

Development of automated data pipelines to extract twitter data, with a sentiment analysis

---

## Table of contents

-   [Description](https://github.com/Dorad-H/Twitter-ETL-Pipeline#description)
-   [ETL pipleline](https://github.com/Dorad-H/Twitter-ETL-Pipeline#extract-transform--load)
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

This ETL pipeline involves using Tweepy, the Twitter API to extract data from Twitter, specifically tweets and replies. The extracted data is then transformed using pandas, a popular data manipulation library in Python, where it is cleaned and reformated into a structured format to fit the database design shown in the E-R Diagram below. The transformed data is loaded into a PostgreSQL database, a scalable and reliable relational database management system.

![alt text](https://github.com/Dorad-H/Twitter_Pipeline/blob/f2fb2f6d67c421ec0cf907aef06637455465ecac/ER%20diagram.png "ER Diagram")
Caption

<figure>
  <img src="https://github.com/Dorad-H/Twitter_Pipeline/blob/f2fb2f6d67c421ec0cf907aef06637455465ecac/ER%20diagram.png"/>
  <figcaption style="text-align=center">This is the caption</figcaption>
</figure>

The pipeline is designed to be automated and monitored using Apache Airflow, an open-source platform for creating, scheduling, and monitoring workflows. We define the pipeline as a DAG (Directed Acyclic Graph), were we schedule of tasks, defined as python functions, and monitor progress. This makes the pipeline more efficient, reliable, and scalable, which is essential when working with large volumes of data.

# Authors

-   [Dorad Hasani](https://studentsunionucl.org/sites/default/files/u198411/image00060.jpeg)
-   [Jan Salcedo](https://github.com/SuperSalcedo22)
-   [Pernelle Gamrowski](https://github.com/pernelleg)
-   [Helen Luhaäär](https://github.com/HelenLB)

[Back to the top](https://github.com/Dorad-H/Twitter-ETL-Pipeline#Twitter-ETL-Pipeline)

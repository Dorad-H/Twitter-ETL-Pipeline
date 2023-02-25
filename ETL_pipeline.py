from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import tweepy
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# ------------------------------------------------------
# Initialise PostgrSQL and Tweepy Credentials
# ------------------------------------------------------
load_dotenv()

# Tweepy credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# PostgreSQL credentials
pg_host = os.getenv('HOST')
pg_db = os.getenv('DATABASE')
pg_user = os.getenv('USER')
pg_pass = os.getenv('PASSWORD')
pg_port = os.getenv('PORT')

# Initial lists used in functions
tweet_list = []
final_dfs = []
company_list = ['SpaceX', 'Microsoft']

# ------------------------------------------------------
# Initialise DAG
# ------------------------------------------------------

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,2,3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    'Twitter_ELT',
    default_args=default_args,
    schedule_interval=timedelta(days=1) # set the schedule to run every day at midnight
)

# ------------------------------------------------------
# Define Functions
# ------------------------------------------------------

def extract_data(**kwargs):
    # global tweet_list
    accounts = kwargs['company_list']
    tweet_list = []

    ti = kwargs['ti']
    # Authenticating the keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Creating the API object
    api = tweepy.API(auth)

    for account in accounts:
        tweet_dict = {}
        try:
            tweets = api.user_timeline(screen_name=account, count=20, exclude_replies=True)
        except:
            print("Exception 1")
            ti.xcom_push(key='tweet_list', value=tweet_list)
            return tweet_list
        now = datetime.now() # Current time
        for tweet in tweets:
            print(tweet.id)
            tweet_time = tweet.created_at.replace(tzinfo=None)
            tweet_dict['created_at'] = datetime.timestamp(tweet_time)
            time_difference = now - tweet_time
            # Check if tweet was posted in the last day
            if time_difference.days == 1:
                tweet_dict['info'] = tweet._json
                tweet_list.append(tweet_dict)
                # finds the replies to the tweet
                try:
                    for tweet2 in tweepy.Cursor(api.search_tweets, q='to:{}'.format(account), since_id=tweet.id, tweet_mode='extended').items():
                        # if it is a reply, writes to a dictionary within the list, with each item containing the text and number of likes
                        print("Exception 1")
                        if tweet2.in_reply_to_status_id == tweet.id:
                            tweet2_dict = {'created_at': datetime.timestamp(tweet2.created_at),
                                            'info': tweet2._json
                                            }
                            tweet_list.append(tweet2_dict)
                except:
                    ti.xcom_push(key='tweet_list', value=tweet_list)
                    return tweet_list

    ti.xcom_push(key='tweet_list', value=tweet_list)
    return tweet_list

def transform_data(**kwargs):
    # Initialise dataframe to contain all information from tweet
    cols = ["tweetId", "companyId", "companyName", "time", "text", "originalTweetID", "favouriteCount", "retweetCount", "hashtagCount", "symbolCount", "mentionCount", "urlCount"]
    data = pd.DataFrame(columns=cols)

    ti = kwargs['ti']
    tweet_list = ti.xcom_pull(key='tweet_list', task_ids='extract_data')

    # Loop over tweets and fill data into dataframe
    for tweet in tweet_list:
        # Company Data  
        companyId = tweet["info"]["user"]["id"] # ID
        companyName = tweet["info"]["user"]["name"] # Name

        # Tweet Data
        tweetID = tweet["info"]["id"] # ID
        tweetTime = tweet["created_at"] # Time
        try:
            tweetText = tweet["info"]["text"] # Tweet Text
        except:
            tweetText = tweet["info"]["full_text"] # Tweet Text
        if tweet["info"]["in_reply_to_status_id"]:
            originalTweetID = tweet["info"]["in_reply_to_status_id"] # ID of original tweet if reply
        else:
            originalTweetID = -1
        favouriteCount = tweet["info"]["favorite_count"] # Number of favourites tweet has recieved
        retweetCount = tweet["info"]["retweet_count"] # Number of retweets tweet has recieved
        hashtagCount = len(tweet["info"]["entities"]["hashtags"]) # Number of hashtages used
        symbolCount = len(tweet["info"]["entities"]["symbols"]) # Number of symbols used
        mentionCount = len(tweet["info"]["entities"]["user_mentions"]) # Number of mentions used
        urlCount = len(tweet["info"]["entities"]["urls"]) # Number of url's in the tweet

        data.loc[tweetID] = [tweetID, companyId, companyName, tweetTime, tweetText, originalTweetID, favouriteCount, retweetCount, hashtagCount, symbolCount, mentionCount, urlCount]

    # Split data into original tweets and replies
    tweet_data = data.loc[(data['originalTweetID'] == -1), :]
    replies = data.loc[(data['originalTweetID'] != -1), :]

    # Initialise the companies dataframe
    companies = pd.DataFrame(columns=["userId", "companyTwitterHandle"])
    # Take all unique account ID's from the original tweet data
    idList = tweet_data.companyId.unique()
    # Find twitter handle associated with the account ID
    for id in idList:
        companyName = tweet_data.loc[(tweet_data.companyId == id),:]['companyName'].unique().tolist()[0]
        companies.loc[id] = [id, companyName]
    
    # Drop columns in tweets and replies to fit the predefined data model
    try:
        tweet_data = tweet_data.drop('originalTweetID', axis=1)
    except:
        print("Tweet data columns already cleaned")

    try:
        replies = replies.loc[:,["tweetId", 'time', 'text', 'originalTweetID', 'favouriteCount', 'retweetCount']]
    except:
        print("Reply data columns already cleaned")
    
    # Create a list of all final dataframes
    final_dfs = [tweet_data,replies,companies]
    final_dfs = [df.to_json(orient='split') for df in final_dfs]
    ti.xcom_push(key='final_dfs', value=final_dfs)
    return final_dfs
    
def load_data(**kwargs):
    # dfList = kwargs['dag_run'].conf.get('final_dfs', None)
    ti = kwargs['ti']
    dfList = ti.xcom_pull(key='final_dfs', task_ids='transform_data')

    dfList = [pd.read_json(df, orient='split') for df in dfList]
    # Connect to the database
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_pass,
        port=pg_port
    )

    # Seperate df_list into individual dataframes
    tweet_df = dfList[0]
    replies_df = dfList[1]
    companies_df = dfList[2]

    # Creating the engine to connect to postgres in order to alter tables
    engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Insert tweet data
    tweet_df.to_sql('tweets', engine, if_exists='append', index=False, schema='twitter_schema')

    # Insert reply data
    replies_df.to_sql('replies', engine, if_exists='append', index=False, schema='twitter_schema')

    # Insert company data
    companies_df.to_sql('companies', engine, if_exists='append', index=False, schema='twitter_schema')

# ------------------------------------------------------
# Initialise PythonOperators
# ------------------------------------------------------

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    op_kwargs= {'company_list': company_list},
    provide_context=True,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_kwargs={'tweet_list': tweet_list},
    provide_context=True,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    op_kwargs={'final_dfs': final_dfs},
    provide_context=True,
    dag=dag
)

# Set task order
# extract_data >> transform_data >> load_data
extract_task.set_downstream(transform_task)
load_task.set_upstream(transform_task)
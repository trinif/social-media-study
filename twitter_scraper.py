import asyncio
from twikit import Client
from dotenv import load_dotenv
import os
import pandas as pd
import time
import ssl
import httpx

# Load .env file
load_dotenv()

# Initialize client
client = Client('en-US')

async def main():

    # Access variables - make diff account?
    
    # Login with cookies
    client.load_cookies('cookies.json')

    # Login manually with .env variables
    # await client.login(
    #     auth_info_1=username,
    #     auth_info_2=email,
    #     password=pwd
    # )

    # client.save_cookies('cookies.json')

    # Get tweets
    # Count var doesn't seem to work?
    tweets = await client.search_tweet('BlackAutisticWomen', 'Latest', count=10)
    i = 0

    df = pd.DataFrame()

    while i < 20:
        # Attributes manually selected

        df2 = pd.DataFrame([{"Text": tweet.text, "Created At": tweet.created_at_datetime, "User ID": tweet.user.id, "Hashtags": tweet.hashtags} for tweet in tweets])
        df = pd.concat([df, df2], ignore_index=True)

        i += 1
        
        if len(df) >= 50:
            df.to_csv('latest_blackautisticwomen_112125.csv', mode='a', header=False)
            df = pd.DataFrame() # reset DF
            time.sleep(15 * 60) # avoid rate limit by waiting 15 minutes
        else:
            tweets = await tweets.next()

    df.to_csv('latest_blackautisticwomen_112125.csv', mode='a', header=False)

# hashtags to try:
# blackautisticgirls
# blackautisticwomen

asyncio.run(main())
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
    username = os.getenv("USERNAME")
    email = os.getenv("EMAIL")
    pwd = os.getenv("PASSWORD")
    
    # Login with cookies
    # client.load_cookies('cookies.json')

    # Login manually
    await client.login(
        auth_info_1=username,
        auth_info_2=email,
        password=pwd
    )

    client.save_cookies('cookies.json')

    # Get tweets
    # Count var doesn't seem to work?
    tweets = await client.search_tweet('Autizzy', 'Latest', count=10)
    i = 0

    df = pd.DataFrame()

    while i < 20:
        # Attributes manually selected

        df2 = pd.DataFrame([{"Text": tweet.text, "Created At": tweet.created_at_datetime, "User ID": tweet.user.id, "Hashtags": tweet.hashtags} for tweet in tweets])
        df = pd.concat([df, df2], ignore_index=True)

        i += 1
        
        if len(df) >= 50:
            df.to_csv('latest_autizzy.csv', mode='a', headers=False)
            df = pd.DataFrame() # reset DF
            time.sleep(15 * 60) # avoid rate limit by waiting 15 minutes
        else:
            tweets = await tweets.next()

    df.to_csv('latest_autizzy.csv', mode='a', headers=False)

asyncio.run(main())
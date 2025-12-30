# Attempting to use twitter_openapi_python

import json
import datetime
import os

from dotenv import load_dotenv
from pathlib import Path
from tweepy_authlib import CookieSessionUserHandler
from twitter_openapi_python import TwitterOpenapiPython

load_dotenv()

# login by tweepy_authlib
# if Path("cookies.json").exists():
#     with open("cookies.json", "r") as f:
#         cookies_dict = json.load(f)
#         if isinstance(cookies_dict, list):
#             cookies_dict = {k["name"]: k["value"] for k in cookies_dict}
# else:
auth_handler = CookieSessionUserHandler(
    screen_name=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)
cookies_dict = auth_handler.get_cookies().get_dict()
print("cookies dict", cookies_dict.keys())

# To extract cookies from Windows (Linux by default)
# If you use tweepy_authlib, you must be on Windows
client = TwitterOpenapiPython()
client.additional_api_headers = {
    "sec-ch-ua-platform": '"Windows"',
}
client.additional_browser_headers = {
    "sec-ch-ua-platform": '"Windows"',
}

# get client from cookies
user = client.get_client_from_cookies(cookies=cookies_dict)

# get tweets from search timeline
response = user.get_tweet_api().get_search_timeline(raw_query="Autizzy", product="Latest")

print(response)
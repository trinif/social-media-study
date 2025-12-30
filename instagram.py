import instaloader
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

L = instaloader.Instaloader()
L.load_session(os.getenv("INSTAGRAM_USERNAME"), {
    "csrftoken": os.getenv("INSTAGRAM_CSRFTOKEN"),
    "sessionid": os.getenv("INSTAGRAM_SESSIONID"),
    "ds_user_id": os.getenv("INSTAGRAM_DSUSERID"),
    "mid": os.getenv("INSTAGRAM_MID"),
    "ig_did": os.getenv("INSTAGRAM_DID")
})

# Force polite mode
L.context.sleep = True
L.context.do_concurrent_queries = False

posts = instaloader.Hashtag.from_name(L.context, "autizzy").get_posts_resumable()

df = pd.DataFrame()

for post in posts:
    # L.download_post(post, "#autizzy") to download post

    # extract date, caption, owner_id, owner_username, url

    df2 = pd.DataFrame([{"Caption": post.caption, "Date": post.date, "User ID": post.owner_id, "Username": post.owner_username, "URL": post.url}])
    df = pd.concat([df, df2], ignore_index=True)

df.to_csv('instagram_autizzy_113025.csv', mode='a', header=False)
import pandas as pd
import asyncio
import os

# parse csv into separate txt files, one for each tweet
# run sentiment analysis
# track by time? possibly see if there are any users in common
def users_in_common():
    csv = "test_output_top_autizzy.csv" # edit file name
    df = pd.read_csv(csv)
    value_counts = df['User ID'].value_counts()
    print(value_counts)

def csv_to_txt():
    csv = "test_output_top_autizzy.csv"
    df = pd.read_csv(csv)

    subdirectory = "top_autizzy_texts"

    # iterate over df and make txt file for each
    # row[3] describes Created At (timestamp)
    for row in df.itertuples():
        file_name = row[3].replace(" ", "_").replace(":", "_") + ".txt" # replace with underscores
        file_path = os.path.join(subdirectory, file_name)
        with open(file_path, "w", encoding="utf-8", errors="replace") as file:
            file.write(row.Text)

def csv_sum():
    csv = "seance_autizzy_test_results.csv"
    df = pd.read_csv(csv)

    print("Sum ", df['nwords'].sum())

async def main():
    # users_in_common()
    # csv_to_txt()
    csv_sum()

asyncio.run(main())
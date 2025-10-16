import statsmodels.api as sm
import asyncio
import pandas as pd
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import os

# read in CSV
def read_csv():
    csv = "seance_autizzy_test_results.csv"
    df = pd.read_csv(csv)
    print(df.shape)

def convert_timestamp(filename: str):
    n = len("2025-08-24_03_05_27") # example string
    datetime_obj = datetime.strptime(filename[:n], "%Y-%m-%d_%H_%M_%S")
    return datetime_obj

def get_seance_components():
    csv = "seance_autizzy_test_results.csv"
    large_df = pd.read_csv(csv)
    indices = [0, 1] + [i for i in range(-20, 0)]
    print(indices)
    df = large_df.iloc[:, indices]
    df['filename'] = df['filename'].apply(convert_timestamp)
    df = df.rename(columns={'filename': 'timestamp'})

    df.to_csv("seance_autizzy_test_results_cleaned.csv")
    

def timestamp_as_num():
    csv = "seance_autizzy_test_results_cleaned.csv"
    df = pd.read_csv(csv, index_col=0)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    min_time = df['timestamp'].min()

    df['timestamp_diff'] = (df['timestamp'] - min_time).dt.total_seconds().astype(int)

    timestamp_diff = df.pop('timestamp_diff')
    df.insert(0, 'timestamp_diff', timestamp_diff)

    df.to_csv("seance_autizzy_test_results_cleaned.csv")

def check_nans_infs():
    csv = "seance_autizzy_test_results_cleaned.csv"
    df = pd.read_csv(csv, index_col=0)

    print(df['timestamp_diff'].isna().sum())  # independent variable (X)
    print(np.isinf(df['timestamp_diff']).sum())
    print(df['timestamp_diff'].dtype)

    for i in range(-20, 0):
        print(df.iloc[:, i].isna().sum())   # dependent variable (y)
        print(np.isinf(df.iloc[:, i]).sum())
        
        print(df.iloc[:, i].dtype)

    df.to_csv("seance_autizzy_test_results_cleaned.csv")

# Poisson distribution
def glm_gaussian():
    csv = "seance_autizzy_test_results_cleaned.csv"
    df = pd.read_csv(csv)
    file_name = "autizzy_glm_gaussian.txt"

    subdirectory = "gaussian_plots"

    for i in range(-20, 0):
        x = sm.add_constant(df[["timestamp_diff"]]) # adds constant for intercept
        y = df.iloc[:, i]
        glm = sm.GLM(y, x, family=sm.families.Gaussian())
        res = glm.fit()
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(res.summary().as_text())
        
        predicted = res.predict(x)
        
        plt.scatter(df["timestamp_diff"], y, label="Data", color="blue", alpha=0.6)
        plt.plot(df["timestamp_diff"], predicted, label="Fitted Line", color="red", linewidth=2)
        
        plt.xlabel("Time since first post (2023)")
        plt.ylabel("Sentiment score")
        plt.title("GLM Fitted Line for " + y.name)
        plt.legend()

        img_name = os.path.join(subdirectory, y.name + ".png")
        plt.savefig(img_name)

        plt.close()

async def main():
    # clean autizzy cleaned output
    # get_seance_components()
    # timestamp_as_num()
    # check_nans_infs()
    glm_gaussian()

asyncio.run(main())

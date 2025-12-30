import statsmodels.api as sm
import asyncio
import pandas as pd
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import os
from scipy import stats
import matplotlib.dates as mdates

# read in CSV
def read_csv():
    csv = "seance_autizzy_test_results.csv"
    df = pd.read_csv(csv)
    print(df.shape)

def convert_timestamp(filename: str):
    n = len("2025-08-24_03_05_27") # example string
    datetime_obj = datetime.strptime(filename[:n], "%Y-%m-%d_%H_%M_%S")
    return datetime_obj

def get_seance_components(csv):
    # for sentiment analysis with more than 20 components
    # large_df = pd.read_csv(csv)
    # indices = [0, 1] + [i for i in range(-20, 0)]
    # print(indices)
    # df = large_df.iloc[:, indices]

    df = pd.read_csv(csv)
    df['filename'] = df['filename'].apply(convert_timestamp)
    df = df.rename(columns={'filename': 'timestamp'})

    index = csv.index('.')
    new_csv = csv[:index] + "_cleaned" + csv[index:]

    df.to_csv(new_csv)

    return new_csv
    

def timestamp_as_num(csv):
    df = pd.read_csv(csv, index_col=0)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    min_time = df['timestamp'].min()

    new_df = pd.DataFrame()

    # in terms of months rather than seconds
    new_df['timestamp_diff'] = ((df['timestamp'] - min_time).dt.days / 30).astype(int)
    new_df['timestamp'] = df['timestamp']
    positive_list = ['joy_component', 'politeness_component', 'positive_adjectives_component', 'positive_nouns_component', 'positive_verbs_component', 'respect_component', 'trust_verbs_component', 'virtue_adverbs_component', 'well_being_component']
    negative_list = ['negative_adjectives_component', 'failure_component', 'fear_and_digust_component']
    new_df['positive'] = df[positive_list].sum(axis=1) / len(positive_list)
    new_df['negative'] = df[negative_list].sum(axis=1) / len(negative_list)

    new_df.to_csv(csv)

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
def glm_gaussian(csv, tag):
    df = pd.read_csv(csv)
    file_name = "seance/" + tag + "_glm_gaussian_positive_and_negative.txt"

    subdirectory = "gaussian_plots_grouped"

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    locator = mdates.MonthLocator(interval=4)
    minor_locator = mdates.MonthLocator()
    formatter = mdates.DateFormatter('%Y-%m-%d')

    x = sm.add_constant(df[["timestamp_diff"]]) # adds constant for intercept
    # TODO: add in another predictor for interaction (girl or woman)
    y = df['positive']
    glm_positive = sm.GLM(y, x, family=sm.families.Gaussian())
    res = glm_positive.fit()
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(res.summary().as_text())
    
    X_null = np.ones((len(y), 1)) 

    null_positive = sm.GLM(y, X_null, family=sm.families.Gaussian()) # X[:,0]*0 creates a column of zeros for the intercept
    null_results = null_positive.fit()
    
    # Perform the Likelihood Ratio Test
    LR = 2 * (res.llf - null_results.llf)

    # Degrees of freedom difference
    df_diff = res.df_model - null_results.df_model

    # p-value
    p_value = stats.chi2.sf(LR, df_diff)
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"LR statistic: {LR:.4f} \n")
        file.write(f"df difference: {df_diff} \n")
        file.write(f"LRT p-value: {p_value:.6g} \n")
        
    predicted = res.predict(x)

    fig, ax = plt.subplots()
    ax.scatter(df["timestamp"], y, label="Data", color="blue", alpha=0.6)
    ax.plot(df["timestamp"], predicted, label="Fitted Line", color="red", linewidth=2)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(axis='x', labelsize=6)

    fig.autofmt_xdate()
        
    ax.set_xlabel("Date of post")
    ax.set_ylabel("Positive sentiment score")
    ax.set_title("GLM Fitted Line for Positive")
    ax.legend()

    img_name = os.path.join(subdirectory, tag + "_positive.png")
    fig.savefig(img_name)

    plt.close(fig)

    y = df['negative']
    glm_negative = sm.GLM(y, x, family=sm.families.Gaussian())
    res = glm_negative.fit()
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(res.summary().as_text())
    
    X_null = np.ones((len(y), 1)) 
    
    null_negative = sm.GLM(y, X_null, family=sm.families.Gaussian()) # X[:,0]*0 creates a column of zeros for the intercept
    null_results = null_negative.fit()
    
    # Perform the Likelihood Ratio Test
    LR = 2 * (res.llf - null_results.llf)

    # Degrees of freedom difference
    df_diff = res.df_model - null_results.df_model

    # p-value
    p_value = stats.chi2.sf(LR, df_diff)
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"LR statistic: {LR:.4f} \n")
        file.write(f"df difference: {df_diff} \n")
        file.write(f"LRT p-value: {p_value:.6g} \n")
        
    predicted = res.predict(x)

    # edited to plot timestamps instead of timestamp_diff
    fig, ax = plt.subplots()
    ax.scatter(df["timestamp"], y, label="Data", color="blue", alpha=0.6)
    ax.plot(df["timestamp"], predicted, label="Fitted Line", color="red", linewidth=2)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(axis='x', labelsize=6)

    fig.autofmt_xdate()
        
    ax.set_xlabel("Date of post")
    ax.set_ylabel("Negative sentiment score")
    ax.set_title("GLM Fitted Line for Negative")
    ax.legend()

    img_name = os.path.join(subdirectory, tag + "_negative.png")
    fig.savefig(img_name)

    plt.close(fig)

async def main():
    # clean output
    # csvs = ["seance/seance_instagram_blackautisticgirl_girls.csv", "seance/seance_instagram_blackautisticwoman_women.csv"]
    # for csv in csvs:
    #     new_csv = get_seance_components(csv)
    #     timestamp_as_num(new_csv)

    # GLM
    csvs_tags = [("seance/seance_instagram_blackautisticgirl_girls_cleaned.csv", "instagram_blackautisticgirl_girls"), ("seance/seance_instagram_blackautisticwoman_women_cleaned.csv", "instagram_blackautisticwoman_women")]
    for (csv, tag) in csvs_tags:
        glm_gaussian(csv, tag)

asyncio.run(main())

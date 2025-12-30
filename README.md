# social-media-study

Research on Black autistic women and girls' social media posts.

# File Structure

- `#blackautisticgirls`: Images from Instagram's `#blackautisticgirls` hashtag
- `gaussian_plots`: Gaussian plots for individual sentiment components from Twitter data
- `gaussian_plots_grouped`: Gaussian plots for positive and negative sentiment groups from various pieces of data, including hashtags from Instagram and the Autizzy hashtag from Twitter
- `seance`: Results from SEANCE's sentiment analysis tools, cleaned to include timestamps, and GLM Gaussian statistical analysis using SEANCE's results
- `csv_to_txt.py`: Helper methods to convert CSV scraped data into individual .txt files for SEANCE analysis, and summing up total word count among social media posts
- `glm.py`: Methods to clean SEANCE results file, assign timestamps, and run GLM Gaussian statistical analysis on cleaned SEANCE file
- `instagram.py`: Python script to scrape data from Instagram per hashtag
- `scraper_v2.py` and `twitter_scraper.py`: Python scripts to scrape data from Twitter/X
- Multiple `.csv` files that contain social media data scraped from Instagram and Twitter/X
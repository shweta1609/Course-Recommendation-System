# GaTech OMSCS Course Recommendation System

## Running the code

Go to `RecommendationSystem/WebUI` and run `flask_demo.py` with `sudo` privileges.

    sudo python flask_demo.py

Open `127.0.0.1:80` in your web browser to see the interface.

## Project Structure

- **dbdumps**: This folder contains 4 MySQL database dumps. `original_reviews` is the DB containing all the scraped values from the OMSCentral website, `original_reviews_with_sentiments` is the same DB with an additional field for sentiment value, as classified by the sentiment analyzer. `more_data.sql` is a DB with data replicated 20 times with random author ID in order to have a larger dataset to work with. `final_clean_db` is the same replicated database with an additional field for sentiments.

- **web-scraper**: This folder contains the code for scraping from the website with Selenium and connecting to the database.

- **sentiment-analysis**: This folder contains code for connecting to the database, parsing all the text reviews, classifying into sentiment classes and storing the results back into the database.

- **RecommendationSystem**: This folder contains 4 recommendation models as indicated below. The subfolder `WebUI` is the user interface built with Flask, along with code to interact with the different models.

Earlier versions of the code are on branches other than `master`.

## Recommendation Models

The recommendation system comprises the following models. More details are available in the project report.  

- **User-based CF**: Based on all our available labels including rating, workload, difficulty, and sentiment label. Requires all dropdowns in the interface to have data entered by the user.  
- **Item-based CF**: User only needs to enter past course names. Similar courses are suggested.  
- **Content based**: User only needs to enter past course names. Courses are suggested based on relevant specialization.  
- **Popular courses**: Handles cold start, where the user has no prior courses, by suggesting the most popular courses so far.  

## Team Members

Shweta Singhal  
Kajal Varma  
Yinghui Dong  
Aarthi Vishwanathan

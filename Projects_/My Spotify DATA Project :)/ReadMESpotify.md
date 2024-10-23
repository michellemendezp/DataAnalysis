#  Spotify Data Analysis and Deployment



##  Project Overview

This project involves analyzing Spotify data using a machine learning model to provide personalized music insights from my data :) so the dataset wont be shared, but I will explain how to access your data and curate the dataset for this model. The workflow includes data preprocessing, model training, and deployment using Streamlit (locally) for an interactive user experience.


##  Workflow

1.  **Data Collection**



3.  **Data Analysis & Model Creation (Jupyter Notebooks)**

-  `AnalysisSpotify.ipynb`: Exploratory Data Analysis (EDA) on Spotify dataset, including feature engineering and visualization. Data preprocessing and training a machine learning model for predicting song preferences.

- Transformation methods used: `StandardScaler`, `PowerTransformer` (Yeo-Johnson method).

  

2.  **ETL, Train, and Test**

-  `ETLSpotify.py`: Extract, transform, and load (ETL) script to process Spotify data.

- Extracts data using the Spotify API and stores it in a local database.

- Applies transformations to prepare the data for training.

-  `train.py`: Script to train the model using the processed data.

-  `test.py`: Script to evaluate model performance on test data.

  

3.  **API Integration and Deployment with Streamlit**

-  `Spotifyapp.py`: Streamlit app that uses the Spotify API to provide an interactive user interface.

- Users can input their Spotify data and receive personalized music recommendations based on their preferences.

- Adjusts the prediction threshold to 0.4 for more controlled sensitivity in song classification.

  

##  Setting Up the Project

  

###  Prerequisites

- Python 3.8+

- Spotify Developer Account

- Spotify Developer API credentials

- Streamlit

- Required libraries:

```
pip install pandas numpy scikit-learn streamlit requests
```

##  Steps to Create the Spotify API

1.  **Create a Spotify Developer Account**

- Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in with your Spotify account.

- Click on "Create an App" to generate a new app.

  

2.  **Obtain Spotify API Credentials**

- After creating the app, go to the "Settings" of your app.

- Note down the `Client ID` and `Client Secret`.

- Set the Redirect URI to `http://localhost:8888/callback`.

  

3.  **Save API Credentials in a `.env` File**

- Create a `.env` file in the root directory of the project.

- Add your Spotify API credentials:

```env

SPOTIFY_CLIENT_ID=your_client_id

SPOTIFY_CLIENT_SECRET=your_client_secret

SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

```
## How to Run the Project Locally

1. **Clone the Repository**
   ```
   git clone https://github.com/yourusername/spotify-analysis.git
   cd spotify-analysis
   ```

2.  **Run the ETL Script**
    
    Extract and transform Spotify data using:

        `SpotifyETL.py` 
        
3.  **Train the Model**
    
   Train the machine learning model using:
        
        `python train.py` 
        
4.  **Test the Model**
    
   Evaluate model performance on test data:
        
        `python test.py` 
        
5.  **Run the Streamlit App**
    
     Launch the Streamlit app to use the Spotify API and interact with the model:

        
        `streamlit run spotifyapp.py` 
        
    -   Open  `http://localhost:8501`  in your browser to access the app.
    -
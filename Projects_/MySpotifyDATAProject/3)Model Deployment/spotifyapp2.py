import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = "http://localhost/"

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Load the trained model and scaler using the updated caching method
@st.cache_resource
def load_model():
    try:
        model = joblib.load('logistic_regression_model.pkl')
        st.write("Model loaded successfully.")
    except Exception as e:
        st.write(f"Error loading model: {e}")
        model = None
    return model

@st.cache_resource
def load_scaler():
    try:
        scaler = joblib.load('scaler.pkl')
        st.write("Scaler loaded successfully.")
    except Exception as e:
        st.write(f"Error loading scaler: {e}")
        scaler = None
    return scaler

# Load the model and scaler
model = load_model()
scaler = load_scaler()

# Function to preprocess user input
def preprocess_input(input_data):
    features = ['acousticness', 'danceability', 'duration', 'energy', 'instrumentalness',
                'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    df = pd.DataFrame([input_data], columns=features)
    if scaler:
        df[features] = scaler.transform(df[features])
    return df

# Fetch song features from Spotify
def get_song_features(song_id):
    features = sp.audio_features(song_id)[0]
    return {
        'acousticness': features['acousticness'],
        'danceability': features['danceability'],
        'duration': features['duration_ms'],
        'energy': features['energy'],
        'instrumentalness': features['instrumentalness'],
        'liveness': features['liveness'],
        'loudness': features['loudness'],
        'speechiness': features['speechiness'],
        'tempo': features['tempo'],
        'valence': features['valence']
    }

# Streamlit app layout
st.title("Spotify Track Likeability Prediction")
st.markdown("### Search for a track to predict if it will be liked:")

# User inputs Spotify track URL or search query
track_query = st.text_input("Enter a track name or Spotify track URL:")
if track_query:
    # Search for the track
    results = sp.search(q=track_query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        track_id = track['id']

        st.write(f"**Selected Track:** {track_name} by {track_artist}")

        # Fetch and display the audio features
        features = get_song_features(track_id)
        st.write("### Audio Features:", features)

        # Predict button
        if st.button("Predict"):
            st.write("Button clicked. Processing input...")
            input_df = preprocess_input(features)
            st.write("Input data after preprocessing:", input_df)
            
            try:
                # Make the prediction using the loaded model
                threshold = 0.4
                prob = model.predict_proba(input_df)[:, 1][0]
                prediction = int(prob >= threshold)
                
                # Display the results
                st.write(f"### Prediction Probability: {prob:.2f}")
                if prediction == 1:
                    st.success("The model predicts that this track will be liked.")
                else:
                    st.warning("The model predicts that this track will not be liked.")
            except Exception as e:
                st.error(f"Error during prediction: {e}")
    else:
        st.write("No track found. Please enter a valid track name or Spotify URL.")

import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

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
    # Define the order of input features as per the training data
    features = ['acousticness', 'danceability', 'duration', 'energy', 'instrumentalness',
                'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    df = pd.DataFrame([input_data], columns=features)
    
    # Apply scaling using the saved scaler
    if scaler:
        df[features] = scaler.transform(df[features])
    return df

# Streamlit app layout
st.title("Spotify Track Likeability Prediction")
st.markdown("### Input the characteristics of a track to predict if it will be liked:")

# Create input fields for each feature
acousticness = st.number_input('Acousticness', min_value=0.0, max_value=1.0, value=0.5)
danceability = st.number_input('Danceability', min_value=0.0, max_value=1.0, value=0.5)
duration = st.number_input('Duration (ms)', min_value=0, value=200000)
energy = st.number_input('Energy', min_value=0.0, max_value=1.0, value=0.5)
instrumentalness = st.number_input('Instrumentalness', min_value=0.0, max_value=1.0, value=0.0)
liveness = st.number_input('Liveness', min_value=0.0, max_value=1.0, value=0.5)
loudness = st.number_input('Loudness (dB)', min_value=-60.0, max_value=0.0, value=-5.0)
speechiness = st.number_input('Speechiness', min_value=0.0, max_value=1.0, value=0.1)
tempo = st.number_input('Tempo', min_value=0.0, max_value=300.0, value=120.0)
valence = st.number_input('Valence', min_value=0.0, max_value=1.0, value=0.5)

# Create a dictionary of inputs
input_data = {
    'acousticness': acousticness,
    'danceability': danceability,
    'duration': duration,
    'energy': energy,
    'instrumentalness': instrumentalness,
    'liveness': liveness,
    'loudness': loudness,
    'speechiness': speechiness,
    'tempo': tempo,
    'valence': valence
}

# Predict button
if st.button("Predict"):
    st.write("Button clicked. Processing input...")
    input_df = preprocess_input(input_data)
    st.write("Input data after preprocessing:", input_df)
    
    try:
        # Make the prediction using the loaded model
        threshold = 0.4  # Use your custom threshold
        prob = model.predict_proba(input_df)[:, 1][0]  # Get probability for the positive class
        prediction = int(prob >= threshold)
        
        # Display the results
        st.write(f"### Prediction Probability: {prob:.2f}")
        if prediction == 1:
            st.success("The model predicts that this track will be liked.")
        else:
            st.warning("The model predicts that this track will not be liked.")
    except Exception as e:
        st.error(f"Error during prediction: {e}")

import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path: str, filename: str) -> pd.DataFrame:
    """
    Load the data from a CSV file.
    
    :param path: Path to the directory containing the data.
    :param filename: Name of the CSV file.
    :return: Loaded DataFrame.
    """
    return pd.read_csv(f"{path}{filename}")

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data: drop unnecessary columns, scale numerical features.
    
    :param df: DataFrame with raw data.
    :return: Preprocessed DataFrame.
    """
    # Drop specified columns
    df = df.drop(columns=['key', 'mode', 'time_signature'])
    
    # Define numerical columns to scale
    numerical_cols = [
        'acousticness', 'danceability', 'duration', 'energy',
        'instrumentalness', 'liveness', 'loudness', 'speechiness',
        'tempo', 'valence'
    ]
    
    # Scale numerical columns
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    # Save the scaler for later use in testing
    import joblib
    joblib.dump(scaler, 'scaler.pkl')
    
    return df

if __name__ == "__main__":
    # Define path and filename
    path = "/Users/michellemendez/Desktop/MICHELLE-WS/DataAnalysis/Projects_/Spotify Analysis/"
    filename = "data_playlist.csv"  # Replace with your actual filename
    
    # Load and preprocess the data
    df = load_data(path, filename)
    df = preprocess_data(df)
    
    # Save the processed data to a new CSV file
    df.to_csv("processed_spotify_data.csv", index=False)
    print("Data preprocessing complete. Saved as 'processed_spotify_data.csv'.")

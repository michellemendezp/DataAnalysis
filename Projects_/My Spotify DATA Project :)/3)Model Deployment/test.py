import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import joblib

def load_data(path: str, filename: str) -> pd.DataFrame:
    """
    Load the data from a CSV file.
    """
    return pd.read_csv(path + filename)

def preprocess_data(df: pd.DataFrame, target: str) -> tuple:
    """
    Preprocess the data: encode and scale.
    """
    # Dummy encoding if needed (replace 'category_columns' with actual columns)
    df = pd.get_dummies(df, drop_first=True)
    
    X = df.drop(columns=[target])
    y = df[target]

    # Load the scaler and transform the test set
    scaler = np.load('scaler.npy', allow_pickle=True).item()
    X_test_scaled = scaler.transform(X)

    return X_test_scaled, y

def evaluate_model(model, X_test: np.ndarray, y_test: pd.Series):
    """
    Evaluate the trained model on the test set.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"ROC AUC: {roc_auc}")

if __name__ == "__main__":
    # Path to the dataset
    path = "/Users/michellemendez/Desktop/MICHELLE-WS/DataAnalysis/Projects_/Spotify Analysis/"
    filename = "data_playlist.csv"
  # Replace with your data filename

    # Load and preprocess data
    df = load_data(path, filename)
    X_test, y_test = preprocess_data(df, 'target_column')  # Replace with actual target column

    # Load the trained model
    model = joblib.load('logistic_regression_model.pkl')
    
    # Evaluate the model
    evaluate_model(model, X_test, y_test)

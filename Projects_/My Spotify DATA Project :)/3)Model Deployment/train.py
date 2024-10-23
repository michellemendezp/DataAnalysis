import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import joblib

def load_processed_data(path: str) -> pd.DataFrame:
    """
    Load the preprocessed data.
    """
    return pd.read_csv(path)

if __name__ == "__main__":
    # Load the preprocessed data
    df = load_processed_data("processed_spotify_data.csv")
    X = df.drop(columns=['label'])  # Adjust if 'label' is your target column
    y = df['label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

    # Train a Logistic Regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'logistic_regression_model.pkl')
    print("Model training complete. Model saved as 'logistic_regression_model.pkl'.")

    # Evaluate the model on the training set with a custom threshold
    threshold = 0.4
    y_train_prob = model.predict_proba(X_train)[:, 1]
    y_train_pred_threshold = (y_train_prob >= threshold).astype(int)

    print("\nTraining Set Performance:")
    print(classification_report(y_train, y_train_pred_threshold))
    print("Training ROC-AUC Score:", roc_auc_score(y_train, y_train_prob))

    # Evaluate the model on the test set with the same threshold
    y_test_prob = model.predict_proba(X_test)[:, 1]
    y_test_pred_threshold = (y_test_prob >= threshold).astype(int)

    print("\nTest Set Performance:")
    print(classification_report(y_test, y_test_pred_threshold))
    print("Test ROC-AUC Score:", roc_auc_score(y_test, y_test_prob))


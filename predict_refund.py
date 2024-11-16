import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)


def train_model(X, y):
    """Train a Random Forest model and return the trained model."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model


def predict_and_save_results(model, new_data_file, output_approved_file, output_flagged_file):
    """
    Use the model to predict refund approvals for new requests.
    Save auto-approved and flagged requests to separate files.
    """
    new_requests = load_data(new_data_file)
    new_requests['refund_approved'] = model.predict(
        new_requests[['purchase_amount', 'return_reason_code', 'customer_return_rate']])

    # Separate auto-approved and flagged requests
    auto_approved = new_requests[new_requests['refund_approved'] == 1]
    flagged = new_requests[new_requests['refund_approved'] == 0]

    # Save results
    auto_approved.to_csv(output_approved_file, index=False)
    flagged.to_csv(output_flagged_file, index=False)
    print(f"Results saved to {output_approved_file} and {output_flagged_file}")


def evaluate_model(model, X_test, y_test):
    """Evaluate the model's accuracy."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    return accuracy


def main():
    # Load historical data
    historical_data_file = 'historical_refund_data.csv'
    new_data_file = 'new_refund_requests.csv'
    output_approved_file = 'auto_approved_refunds.csv'
    output_flagged_file = 'flagged_refunds.csv'

    data = load_data(historical_data_file)

    # Features and target
    X = data[['purchase_amount', 'return_reason_code', 'customer_return_rate']]
    y = data['refund_approved']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

    # Predict and save results
    predict_and_save_results(model, new_data_file, output_approved_file, output_flagged_file)


if __name__ == "__main__":
    main()

from flask import Flask, request
import joblib

app = Flask(__name__)


@app.route("/predict")
def predict():
    """
    Make a prediction based on the provided query parameters.

    Args:
        vol_moving_avg (str): Volume moving average value.
        adj_close_rolling_med (str): Adjusted close rolling median value.

    Returns:
        str: The predicted integer value.
    """

    # Get the query parameters
    vol_moving_avg = request.args.get("vol_moving_avg")
    adj_close_rolling_med = request.args.get("adj_close_rolling_med")
    if not vol_moving_avg or not adj_close_rolling_med:
        return "Missing parameters", 400

    # Load the model
    model = joblib.load("data/ml_training/model.joblib")

    # Make prediction
    prediction = model.predict([[vol_moving_avg, adj_close_rolling_med]])
    # Return the prediction
    return str(int(prediction[0]))


if __name__ == "__main__":
    app.run()

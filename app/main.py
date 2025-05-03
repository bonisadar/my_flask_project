
# ======================= IMPORTS =======================
import pickle
import os
from flask import Flask, request, jsonify
import logging
import re
import numpy as np
import joblib
from utils.preprocess import preprocess_url_single
from models.predictor import load_model, predict

from schemas.predict import URLRequest 

from utils.preprocess import preprocess_url_single
from models.predictor import load_model, predict

# Optional: Use Pydantic here if you want strict validation
# from schemas.predict import URLRequest

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== Load model on startup ==========
model = load_model()
if model:
    logger.info("Model loaded successfully")
else:
    logger.error("Model failed to load")


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Flask app running"})


@app.route("/predict", methods=["POST"])
def predict_url():
    global model
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' in request"}), 400

        url = str(data["url"])
        prediction = predict(model, url)
        label = "Legitimate" if prediction == 1 else "Phishing"
        return jsonify({"prediction": label})
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
import re

# Load the trained model
model = tf.keras.models.load_model("password_strength_model.h5")

# Initialize Flask app
app = Flask(__name__)

# Feature extraction function
def extract_features(password):
    length = len(password)
    digits = len(re.findall(r'\d', password))
    uppercase = len(re.findall(r'[A-Z]', password))
    special_chars = len(re.findall(r'[@$!%*?&#]', password))
    return np.array([[length, digits, uppercase, special_chars]])

# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for password strength analysis
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Password is required"}), 400

    # Predict password strength
    features = extract_features(password)
    prediction = model.predict(features)
    strength_label = ["Weak", "Medium", "Strong"][np.argmax(prediction)]

    return jsonify({"password": password, "strength": strength_label})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

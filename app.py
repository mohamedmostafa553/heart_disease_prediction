import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, send_from_directory

# Set environment variable to disable oneDNN if needed
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__, static_url_path='', static_folder='static')

# Load the pre-trained model
model_path = "model.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {model_path}: {e}")

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.form

        # List of expected features
        expected_features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 
                             'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        # Extract features from the request data
        features = []
        for feature in expected_features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            features.append(float(data[feature]))

        features = np.array(features).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)

        # Interpret prediction
        if prediction[0][0] > 0.5:
            result = "you have heart disease"
        else:
            result = "you do not have any disease"

        # Return prediction
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

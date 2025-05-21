import numpy as np
import tensorflow as tf
from joblib import load
import os

LOOK_BACK = 288
HORIZON = 12

def load_model_and_scaler():
    model_path = os.path.join(os.path.dirname(__file__), 'pm2_5_model.keras')
    scaler_path = os.path.join(os.path.dirname(__file__), 'pm2_5_minmax.pkl')
    
    model = tf.keras.models.load_model(model_path)
    scaler = load(scaler_path)
    
    return model, scaler

def predict_pm2_5(raw_input_sequence, model, scaler):
    input_array = np.array(raw_input_sequence).reshape((len(raw_input_sequence), 1))
    scaled_input = scaler.transform(input_array)
    model_input = scaled_input.reshape((1, LOOK_BACK, 1))
    
    raw_prediction = model.predict(model_input)
    
    prediction_to_inverse_scale = raw_prediction.reshape((HORIZON, 1))
    unscaled_prediction = scaler.inverse_transform(prediction_to_inverse_scale)
    final_prediction = unscaled_prediction.flatten()
    
    return final_prediction 
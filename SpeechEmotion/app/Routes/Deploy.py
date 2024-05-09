from flask import Flask, request, jsonify,Blueprint,json
from tensorflow.keras.models import model_from_json, Sequential
from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, Dropout, Flatten, Dense

import tensorflow.keras.layers as L
from sklearn.preprocessing import LabelEncoder
# from app.models import Emotions, Records
import numpy as np
import tensorflow as tf
import librosa
import pickle
import os
import base64
from io import BytesIO
import uuid
import tempfile

# Custom object dictionary
custom_objects = {
    'Sequential': Sequential,
    'Conv1D': Conv1D,
    'BatchNormalization': BatchNormalization,
    'MaxPooling1D': MaxPooling1D,
    'Dropout': Dropout,
    'Flatten': Flatten,
    'Dense': Dense
}
# Create a Blueprint for deployment
deploy_bp = Blueprint('Deploy', __name__, url_prefix='/model')


json_file = open(r'SpeechEmotion\app\kaggle\CNN_model.json', 'r')
loaded_model_json = json_file.read()
#print(loaded_model_json)
json_file.close()
loaded_model = model_from_json(loaded_model_json, custom_objects=custom_objects)
# load weights into new model
loaded_model.load_weights(r"SpeechEmotion\app\kaggle\best_model1_weights.h5")


# Load the scaler and encoder
with open(r'SpeechEmotion\app\Routes\scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)

with open(r'SpeechEmotion\app\Routes\encoder2.pickle', 'rb') as f:
    encoder2 = pickle.load(f)

# Define feature extraction functions
def zcr(data, frame_length, hop_length):
    zcr = librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(zcr)

def rmse(data, frame_length=2048, hop_length=512):
    rmse = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(rmse)

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfcc = librosa.feature.mfcc(y=data, sr=sr)
    return np.squeeze(mfcc.T) if not flatten else np.ravel(mfcc.T)

def extract_features(data, sr=22050, frame_length=2048, hop_length=512):
    result = np.array([])
    result = np.hstack((result,
                        zcr(data, frame_length, hop_length),
                        rmse(data, frame_length, hop_length),
                        mfcc(data, sr, frame_length, hop_length)
                    ))
    return result

def get_predict_feat(path):
    d, s_rate = librosa.load(path, duration=2.5, offset=0.6)
    res = extract_features(d)
    result = np.array(res)
    result = np.reshape(result, newshape=(1, 2376))
    i_result = scaler2.transform(result)
    final_result = np.expand_dims(i_result, axis=2)
    return final_result



def prediction(path):
    res = get_predict_feat(path)
    predictions = loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    return y_pred[0][0]

# Create a new dataset
def store_record(file, prediction_result):
    emotion_folders = {
        'happy':'Happy',
        'sad':'Sad',
        'angry':'Angry',
        'neutral':'Neutral',
        'surprised':'Surprised',
        'disgusted':'Disgusted',
        'fearful':'Fearful'
    }

    # Check if the prediction_result matches any emotion
    if prediction_result.lower() in emotion_folders:

        # Get the folder name for the emotion
        folder_name = emotion_folders[prediction_result.lower()]
        
        # Path to the folder where the record will be stored
        folder_path = os.path.join('Dataset', folder_name)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Generate a unique filename for the record
        record_filename = str(uuid.uuid4()) + '.wav'

        # Save the file in the folder with the unique filename
        file.save(os.path.join(folder_path, record_filename))




# Prediction endpoint
@deploy_bp.route('/predict-emotion',methods=['POST'])
def predict():
    file = request.files['file']
    
    if not file:
        return jsonify({'error': 'Empty file'})

    #file.save('temp.wav')
    prediction_result = prediction(file)

    store_record(file, prediction_result)

    return jsonify({'emotion':prediction_result})


@deploy_bp.route('/predict-emotion-real-time', methods=['POST'])
def predict_live():
    audio_data = request.stream.read()  # Read audio data from the request stream

    if not audio_data:
        return jsonify({'error': 'Empty audio data'})

    # Create a temporary file to store the audio data
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file_name = temp_audio_file.name

    # You can now pass audio_file to your prediction function
    prediction_result = prediction(temp_audio_file_name)

    store_record(temp_audio_file_name, prediction_result)

    return jsonify({'emotion': prediction_result})
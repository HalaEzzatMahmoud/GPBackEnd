from flask import Flask, request, jsonify,Blueprint,json
from tensorflow.keras.models import model_from_json, Sequential
from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, Dropout, Flatten, Dense

import tensorflow.keras.layers as L
from sklearn.preprocessing import LabelEncoder
from app.Routes.Records import PredictedRecordSave
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
deploy_bp = Blueprint('Deploy', __name__, url_prefix='/Deploy')


json_file = open(r'SpeechEmotion\app\kaggle\CNN_model.json', 'r')
loaded_model_json = json_file.read()
#print(loaded_model_json)
json_file.close()
loaded_model = model_from_json(loaded_model_json, custom_objects=custom_objects)
# load weights into new model
loaded_model.load_weights(r"SpeechEmotion\app\kaggle\best_model1_weights.h5")


# Load the scaler and encoder
with open(r'SpeechEmotion\app\kaggle\scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)

with open(r'SpeechEmotion\app\kaggle\encoder2.pickle', 'rb') as f:
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


# Prediction endpoint for employee
@deploy_bp.route('/predict-emotion/<int:user_id>',methods=['POST'])
def predict(user_id):
    print("Predict endpoint accessed") 
    file = request.files['file']
    
    if not file:
        return jsonify({'error': 'Empty file'})

    prediction_result = prediction(file)
    #print("00000000000000000000000",file)
    new_record =PredictedRecordSave(file, prediction_result,user_id)

    return jsonify({
        'message': 'File and prediction result saved successfully.',
        'record_id': new_record.recordID,
        'file_path': new_record.record_path,
        'emotion': new_record.emotion.emotion,
        'userID':user_id
    })



# save record form Client without the prediction result by using the user ID
def storeRecordClient(file, user_id):
    try:
        # Path to the folder where the user's records will be stored
        user_folder_path = os.path.join('UsersRecords', str(user_id))

        # Create the user's folder if it doesn't exist
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
            print("User folder created")


        # Generate a unique filename for the record
        record_filename = str(uuid.uuid4()) + f'__{user_id}.wav'

        # Save the file in the user's folder with the unique filename
        file_path = os.path.join(user_folder_path, record_filename)
        file.save(file_path)

        return file_path
    except Exception as e:
        return str(e)    

# send record and saving it 'form Client'
@deploy_bp.route('/save-record-client/<int:user_id>',methods=['POST'])
def save_record_client(user_id):
    file = request.files['file']
    user_id = request.view_args.get('user_id') 
    
    if not file or user_id is None:
        return jsonify({'error': 'Empty'})

    savedRecord = storeRecordClient(file, user_id)

    return jsonify({'emotion':'File saved successfully ','file_path':savedRecord}) 




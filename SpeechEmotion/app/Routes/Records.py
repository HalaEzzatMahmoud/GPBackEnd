from app.database import db 
from app.models import Emotions, Records
from flask import Blueprint, request,jsonify,abort
from werkzeug.utils import secure_filename
import os
import uuid


# Create a Blueprint for deployment
Record_bp = Blueprint('Record', __name__, url_prefix='/Records')


def storeRecordClient(file, user_id):
    try:
        # Path to the folder where the user's records will be stored
        user_folder_path = os.path.join('UsersRecords', str(user_id))

        # Create the user's folder if it doesn't exist
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
            print("User folder created")

        # Generate a unique filename for the record
        record_filename = f'UserRecord__{user_id}.wav'

        # Save the file in the user's folder with the unique filename
        file_path = os.path.join(user_folder_path, record_filename)
        file.save(file_path)

        return file_path
    except Exception as e:
        return str(e) 

# send record and saving it 'form Client'
@Record_bp.route('/save-record-client/<int:user_id>',methods=['POST'])
def save_record_client(user_id):
    file = request.files['file']
    
    if not file or user_id is None: 
        return jsonify({'error': 'Empty'})

    savedRecord = storeRecordClient(file, user_id)

    return jsonify({'Message':'File saved successfully ','file_path':savedRecord}) 


#Save Predicted file and emotion for employee
def PredictedRecordSave(file,prediction_result,user_id):
    emotion = Emotions.query.filter_by(emotion=prediction_result).first()
    # Extract the filename and ensure its safety
    filename = secure_filename(file.filename)
    if not emotion:
        # If it doesn't exist, create a new emotion record
        emotion = Emotions(emotion=prediction_result)
        db.session.add(emotion)
        db.session.commit()

    # Save the record data and link it to the emotion
    new_record = Records(record_path=filename, emotion_id=emotion.emotionID,userID=user_id)
    db.session.add(new_record)
    db.session.commit()

    return new_record
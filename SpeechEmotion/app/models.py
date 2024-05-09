from .database import db

class Users(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    DateOfBirth = db.Column(db.String(50), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('Gender.GenderID'))
    gender = db.relationship('Gender', backref='Users')


    def to_dict(self):
        return {
            'user_id':self.UserID,
            'first_name':self.FirstName,
            'last_name':self.LastName,
            'user_name':self.UserName,
            'password':self.Password,
            'Email':self.Email,
            'DateOfBirth':self.DateOfBirth,
            'gender': self.gender_id,
        }

class Gender(db.Model):
    __tablename__ = 'Gender'
    GenderID = db.Column(db.Integer, primary_key=True)
    GenderName = db.Column(db.String(50), nullable=False)

'''class Emotions(db.Model):
    __tablename__ = 'emotion'
    emotionID = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)    


class Records(db.Model):
    __tablename__ = 'record'
    recordID = db.Column(db.Integer, primary_key=True)
    record_data = db.Column(db.BLOB, nullable=False) 
    emotion_id = db.Column(db.Integer, db.ForeignKey('emotion.emotionID'), nullable=False)
    emotion = db.relationship('Emotions', backref='Records')'''    
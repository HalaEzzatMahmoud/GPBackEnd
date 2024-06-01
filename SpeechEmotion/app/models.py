from .database import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    UserName = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    DateOfBirth = db.Column(db.String(255), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('Gender.GenderID'))
    gender = db.relationship('Gender', backref='users')
    roleID = db.Column(db.Integer, db.ForeignKey('role.roleID'))
    role = db.relationship('Role', backref='users')


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
            'roleID' : self.roleID
        }

class Gender(db.Model):
    __tablename__ = 'Gender'
    GenderID = db.Column(db.Integer, primary_key=True)
    GenderName = db.Column(db.String(250), nullable=False)

class Role(db.Model):
    __tablename__ = 'role'
    roleID = db.Column(db.Integer, primary_key=True)
    roleType = db.Column(db.String(250), nullable=False)


class News(db.Model):
    __tablename__ = 'news'
    newsID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(350))
    date1 = db.Column(db.DateTime, default=datetime.utcnow)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    user = db.relationship('Users', foreign_keys=[UserID], backref=db.backref('news', lazy=True))

class Complaints(db.Model):
    __tablename__ = 'complaints'   
    ComplaintID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    DateCreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    Status = db.Column(db.String(50), default='Open')
    Priority = db.Column(db.String(50), default='Medium')
    Phone = db.Column(db.String(100)) 
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    user = db.relationship('Users', foreign_keys=[UserID], backref=db.backref('complaints', lazy=True))



class Emotions(db.Model):
    __tablename__ = 'emotion'
    emotionID = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)    


class Records(db.Model):
    __tablename__ = 'record'
    recordID = db.Column(db.Integer, primary_key=True)
    record_path = db.Column(db.String(255), nullable=False) 
    emotion_id = db.Column(db.Integer, db.ForeignKey('emotion.emotionID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    user = db.relationship('Users', foreign_keys=[userID], backref=db.backref('record', lazy=True))
    emotion = db.relationship('Emotions', backref='Records')
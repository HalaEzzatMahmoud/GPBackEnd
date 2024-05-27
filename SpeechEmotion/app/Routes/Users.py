from app.database import db 
from app.models import Users
from flask import Blueprint, request,jsonify,abort
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash

users_bp = Blueprint('users',__name__, url_prefix='/users')

@users_bp.route('/SignUp',methods=['POST'])
def register():
    data = request.get_json()  

    hashed_password = generate_password_hash(data['Password'])

    new_user = Users(
        FirstName = data['FirstName'],
        LastName = data['LastName'],
        UserName = data['UserName'],
        Password=hashed_password, 
        Email = data['Email'],
        DateOfBirth = data['DateOfBirth'],
        gender_id = data['gender_id'], 
        roleID = data.get('role', 2) # 2 for client
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict())


@users_bp.route('/Login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['UserName']
    password = data['Password']

    if not username or not password:
        return abort(400, "Username and password are required.")

    user = Users.query.filter_by(UserName=username).first()

    if user and check_password_hash(user.Password, password):
        return jsonify({'message': 'Login successful.','role_id':user.roleID,'user_id': user.UserID})
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

'''@users_bp.route('/retrive-histroy/<int:user_id>', methods=['POST'])
def Histroy(user_id):'''
    

'''@users_bp.route('/<int:user_id>',methods=['PUT'])    
def Update_user(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.get_json()

    user.FirstName = data.get('FirstName', Users.FirstName)
    user.LastName = data.get('LastName',Users.LastName)
    user.UserName = data.get('UserName',Users.UserName)
    user.Password = data.get('Password',Users.Password)
    user.Email = data.get('Email',Users.Email)
    user.DateOfBirth = data.get('DateOfBirth',Users.DateOfBirth)
    user.gender_id = data.get('gender_id',Users.gender_id)
    


    db.session.commit()
    return jsonify(user.to_dict())


@users_bp.route('/<int:user_id>',methods=['DELETE'])  
def Delete_user(user_id):
    user = Users.query.get_or_404(user_id)

    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User successfully deleted'})'''


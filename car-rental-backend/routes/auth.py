from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.objects(username=data['username']).first():
        return jsonify(msg="Username already exists"), 400
    user = User(username=data['username'], password=generate_password_hash(data['password']))
    user.save()
    return jsonify(msg="User registered")

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify(msg="Invalid credentials"), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash,generate_password_hash
import validators
from src.database import User, db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.route('/register', methods=['GET','POST'])
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "password is too short"}), HTTP_400_BAD_REQUEST 

    if len(username) < 3:
        return jsonify({'error': "username is too short"}), HTTP_400_BAD_REQUEST 

    if not username.isalnum() or " " in username: 
        return jsonify({'error': "username should have no spaces and should be alphanumeric"}), HTTP_400_BAD_REQUEST 

    if not validators.email(email):
        return jsonify({'error': "email not valid"}), HTTP_400_BAD_REQUEST 

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "email exists"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return ({
        'message':"User created",
        'user': {
            'username': username, "email": email
        }
    }),HTTP_201_CREATED


@auth.route("/login", methods=['GET', 'POST'])
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        validate_password = check_password_hash(user.password, password)

        if validate_password:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            
            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }
            })

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.route('/token/refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK

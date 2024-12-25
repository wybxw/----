from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db, bcrypt
from models import User
from flasgger import swag_from

class UserRegisterAPI(Resource):
    @swag_from({
        'tags': ['用户管理'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string', 'description': '用户名'},
                        'email': {'type': 'string', 'description': '邮箱'},
                        'password': {'type': 'string', 'description': '密码'}
                    }
                }
            }
        ],
        'responses': {
            '201': {
                'description': '用户注册成功'
            },
            '400': {
                'description': '用户名或邮箱已存在'
            },
            '500': {
                'description': '内部服务器错误'
            }
        }
    })
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if User.query.filter_by(username=username).first():
                return make_response(jsonify({'message': '用户名已存在'}), 400)
            if User.query.filter_by(email=email).first():
                return make_response(jsonify({'message': '邮箱已存在'}), 400)

            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify({'message': '用户注册成功'}), 201)
        except Exception as e:
            print(f"Error: {e}")
            return make_response(jsonify({'message': '内部服务器错误'}), 500)

class UserLoginAPI(Resource):
    @swag_from({
        'tags': ['用户管理'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string', 'description': '用户名'},
                        'password': {'type': 'string', 'description': '密码'}
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': '登录成功，返回访问令牌'
            },
            '401': {
                'description': '用户名或密码错误'
            },
            '500': {
                'description': '内部服务器错误'
            }
        }
    })
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if not user or not bcrypt.check_password_hash(user.password_hash, password):
                return make_response(jsonify({'message': '用户名或密码错误'}), 401)

            access_token = create_access_token(identity=str(user.id))  # 确保 identity 是字符串类型
            return make_response(jsonify({'access_token': access_token}), 200)
        except Exception as e:
            print(f"Error: {e}")
            return make_response(jsonify({'message': '内部服务器错误'}), 500)

class UserProfileAPI(Resource):
    @swag_from({
        'tags': ['用户管理'],
        'security': [{'Bearer': []}],
        'responses': {
            '200': {
                'description': '返回用户信息'
            },
            '404': {
                'description': '用户未找到'
            },
            '500': {
                'description': '内部服务器错误'
            }
        }
    })
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return make_response(jsonify({'message': '用户未找到'}), 404)

            return make_response(jsonify({
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }), 200)
        except Exception as e:
            print(f"Error: {e}")
            return make_response(jsonify({'message': '内部服务器错误'}), 500)
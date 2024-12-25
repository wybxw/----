import os
from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.utils import secure_filename
from extensions import app, db,api
from models import DataSources, DisasterData
import hashlib
from 数据编解码模块 import decode_integrated_code

# 配置文件上传路径
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# # 数据来源管理
# class DataSourcesAPI(Resource):
#     @swag_from({
#         'tags': ['数据来源'],
#         'parameters': [
#             {
#                 'name': 'source_id',
#                 'in': 'path',
#                 'type': 'integer',
#                 'required': False,
#                 'description': '数据来源ID'
#             }
#         ],
#         'responses': {
#             '200': {
#                 'description': '返回数据来源列表或单个数据来源'
#             }
#         }
#     })
#     def get(self, source_id=None):
#         if source_id:
#             source = DataSources.query.get(source_id)
#             return jsonify(source)
#         else:
#             sources = DataSources.query.all()
#             return jsonify(sources)

#     @swag_from({
#         'tags': ['数据来源'],
#         'parameters': [
#             {
#                 'name': 'body',
#                 'in': 'body',
#                 'required': True,
#                 'schema': {
#                     'type': 'object',
#                     'properties': {
#                         'name': {'type': 'string', 'description': '名称'},
#                         'type': {'type': 'string', 'description': '类型'},
#                         'description': {'type': 'string', 'description': '描述'}
#                     }
#                 }
#             }
#         ],
#         'responses': {
#             '200': {
#                 'description': '数据来源添加成功'
#             }
#         }
#     })
#     def post(self):
#         data = request.get_json()
#         new_source = DataSources(**data)
#         db.session.add(new_source)
#         db.session.commit()
#         return jsonify({'message': '数据来源添加成功'})

#     @swag_from({
#         'tags': ['数据来源'],
#         'parameters': [
#             {
#                 'name': 'source_id',
#                 'in': 'path',
#                 'type': 'integer',
#                 'required': True,
#                 'description': '数据来源ID'
#             },
#             {
#                 'name': 'body',
#                 'in': 'body',
#                 'required': True,
#                 'schema': {
#                     'type': 'object',
#                     'properties': {
#                         'name': {'type': 'string', 'description': '名称'},
#                         'type': {'type': 'string', 'description': '类型'},
#                         'description': {'type': 'string', 'description': '描述'}
#                     }
#                 }
#             }
#         ],
#         'responses': {
#             '200': {
#                 'description': '数据来源更新成功'
#             }
#         }
#     })
#     def put(self, source_id):
#         source = DataSources.query.get(source_id)
#         if not source:
#             return jsonify({'message': '数据来源未找到'})
#         update_data = request.get_json()
#         for key, value in update_data.items():
#             setattr(source, key, value)
#         db.session.commit()
#         return jsonify({'message': '数据来源更新成功'})

#     @swag_from({
#         'tags': ['数据来源'],
#         'parameters': [
#             {
#                 'name': 'source_id',
#                 'in': 'path',
#                 'type': 'integer',
#                 'required': True,
#                 'description': '数据来源ID'
#             }
#         ],
#         'responses': {
#             '200': {
#                 'description': '数据来源删除成功'
#             }
#         }
#     })
#     def delete(self, source_id):
#         source = DataSources.query.get(source_id)
#         if not source:
#             return jsonify({'message': '数据来源未找到'})
#         db.session.delete(source)
#         db.session.commit()
#         return jsonify({'message': '数据来源删除成功'})

# 数据接入管理
class DataAccessAPI(Resource):
    @swag_from({
        'tags': ['数据接入'],
        'parameters': [
            {
                'name': 'id',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': '一体化编码串'
            },
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': '数据文件'
            }
        ],
        'responses': {
            '200': {
                'description': '数据接入成功'
            }
        }
    })
    def post(self):
        id = request.form.get('id')
        file = request.files.get('file')

        if not id or not file:
            return jsonify({'message': '缺少必要的参数'}), 400

        # 计算文件的MD5值并用作文件名

        def calculate_md5(file):
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
            file.seek(0)  # Reset file pointer to the beginning
            return hash_md5.hexdigest()

        md5_filename = calculate_md5(file) + os.path.splitext(file.filename)[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], md5_filename)
        file.save(file_path)

        # 调用解码模块
        with app.app_context():
            disaster_data = decode_integrated_code(id,file_path)
            disaster_data.file_path = file_path
            db.session.add(disaster_data)
            db.session.commit()

        return jsonify({'message': '数据接入成功', 'file_path': file_path})


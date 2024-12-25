from flask import request, jsonify, make_response
from flask_restful import Resource
from flasgger import swag_from
from models import db, DisasterData

# 灾情数据管理
class DisasterDataAPI(Resource):
    @swag_from({
        'tags': ['灾情数据'],
        'parameters': [
            {
                'name': 'province',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': '省'
            },
            {
                'name': 'city',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': '城市'
            },
            {
                'name': 'disaster_category',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': '灾情大类'
            },
            {
                'name': 'start_date',
                'in': 'query',
                'type': 'string',
                'format': 'date-time',
                'required': False,
                'description': '开始日期'
            },
            {
                'name': 'end_date',
                'in': 'query',
                'type': 'string',
                'format': 'date-time',
                'required': False,
                'description': '结束日期'
            },
            {
                'name': 'page',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': '页码'
            },
            {
                'name': 'per_page',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': '每页数量'
            },{
                'name': 'uploader_id',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': '上传人ID'
            },{
                'name': 'source_id',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': '来源ID'
            }
        ],
        'responses': {
            '200': {
                'description': '返回灾情数据列表'
            }
        }
    })
    def get(self):
        # 获取查询参数
        province = request.args.get('province')
        city = request.args.get('city')
        disaster_category = request.args.get('disaster_category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        uploader_id = request.args.get('uploader_id')
        source_id = request.args.get('source_id')
        # 构建查询条件
        query = DisasterData.query
        if province:
            query = query.filter(DisasterData.province == province)
        if city:
            query = query.filter(DisasterData.city == city)
        if disaster_category:
            query = query.filter(DisasterData.disaster_category == disaster_category)
        if start_date:
            query = query.filter(DisasterData.upload_date >= start_date)
        if end_date:
            query = query.filter(DisasterData.upload_date <= end_date)
        if uploader_id:
            query = query.filter(DisasterData.uploader_id == uploader_id)
        if source_id:
            query = query.filter(DisasterData.source_id == source_id)
        # 分页查询
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        data = pagination.items

        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': pagination.per_page,
            'data': [d.to_dict() for d in data]
        })

class DisasterDataDetailAPI(Resource):
    @swag_from({
        'tags': ['灾情数据'],
        'parameters': [
            {
                'name': 'data_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': '灾情数据ID'
            }
        ],
        'responses': {
            '200': {
                'description': '返回单个灾情数据'
            },
            '404': {
                'description': '灾情数据未找到'
            }
        }
    })
    def get(self, data_id):
        data = DisasterData.query.get(data_id)
        if not data:
            return make_response(jsonify({'message': '灾情数据未找到'}), 404)
        return jsonify(data.to_dict())

    @swag_from({
        'tags': ['灾情数据'],
        'parameters': [
            {
                'name': 'data_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': '灾情数据ID'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'province': {'type': 'string', 'description': '省'},
                        'city': {'type': 'string', 'description': '城市'},
                        'town': {'type': 'string', 'description': '镇'},
                        'village': {'type': 'string', 'description': '村/居委会'},
                        'disaster_category': {'type': 'string', 'description': '灾情大类'},
                        'upload_date': {'type': 'string', 'format': 'date-time', 'description': '上传日期'},
                        'update_date': {'type': 'string', 'format': 'date-time', 'description': '更新日期'},
                        'uploader_id': {'type': 'integer', 'description': '上传人ID'},
                        'source_id': {'type': 'integer', 'description': '来源ID'},
                        'timestamp': {'type': 'string', 'format': 'date-time', 'description': '时间戳'},
                        'expiry_date': {'type': 'string', 'format': 'date-time', 'description': '过期日期'},
                        'street': {'type': 'string', 'description': '街道'},
                        'source': {'type': 'string', 'description': '来源'},
                        'carrier': {'type': 'string', 'description': '载体'},
                        'disaster_subcategory': {'type': 'string', 'description': '灾情子类'},
                        'disaster_indicator': {'type': 'string', 'description': '灾情指标'},
                        'data_path': {'type': 'string', 'description': '数据路径'}
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': '灾情数据更新成功'
            },
            '404': {
                'description': '灾情数据未找到'
            }
        }
    })
    def put(self, data_id):
        data = DisasterData.query.get(data_id)
        if not data:
            return make_response(jsonify({'message': '灾情数据未找到'}), 404)

        update_data = request.get_json()
        for key, value in update_data.items():
            setattr(data, key, value)
        db.session.commit()
        return make_response(jsonify({'message': '灾情数据更新成功'}), 200)

    @swag_from({
        'tags': ['灾情数据'],
        'parameters': [
            {
                'name': 'data_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': '灾情数据ID'
            }
        ],
        'responses': {
            '200': {
                'description': '灾情数据删除成功'
            },
            '404': {
                'description': '灾情数据未找到'
            }
        }
    })
    def delete(self, data_id):
        data = DisasterData.query.get(data_id)
        if not data:
            return make_response(jsonify({'message': '灾情数据未找到'}), 404)

        db.session.delete(data)
        db.session.commit()
        return make_response(jsonify({'message': '灾情数据删除成功'}), 200)
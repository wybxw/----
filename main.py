from datetime import datetime
import pytz
from extensions import app, api

def get_utc8_time():
    utc_time = datetime.utcnow()
    utc8_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
    return utc8_time

# 导入模块
from 数据接入模块 import DataAccessAPI
from 数据管理模块 import DisasterDataAPI,DisasterDataDetailAPI
from 用户管理模块 import UserRegisterAPI, UserLoginAPI, UserProfileAPI

# 注册 API 路由
api.add_resource(DataAccessAPI, '/data_access')

# 注册 API 路由
api.add_resource(UserRegisterAPI, '/register')
api.add_resource(UserLoginAPI, '/login')
api.add_resource(UserProfileAPI, '/profile')
# 注册 API 路由
api.add_resource(DisasterDataAPI, '/disaster_data')
api.add_resource(DisasterDataDetailAPI, '/disaster_data/<data_id>')


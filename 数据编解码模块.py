# 数据编解码模块.py
from datetime import datetime
from extensions import app, db
from models import AreaCode2024, DisasterData

def get_area_info(code):
    area_info = {}
    levels = ['province', 'city', 'county', 'street', 'committee']
    code_patterns = [
        code[:2] + '0000000000',
        code[:4] + '00000000',
        code[:6] + '000000',
        code[:9] + '000',
        code
    ]

    for level, pattern in zip(levels, code_patterns):
        result = AreaCode2024.query.filter_by(code=int(pattern)).first()
        if result:
            area_info[level] = {
                'code': result.code,
                'name': result.name,
                'level': result.level,
                'pcode': result.pcode,
                'category': result.category
            }

    return area_info

# 编码规范中的对照表
source_code_map = {
    '1': {
        '00': '前方地震应急指挥部',
        '01': '后方地震应急指挥部',
        '20': '应急指挥技术系统',
        '21': '社会服务工程应急救援系统',
        '40': '危险区预评估工作组',
        '41': '地震应急指挥技术协调组',
        '42': '震后政府信息支持工作项目组',
        '80': '灾情快速上报接收处理系统',
        '81': '地方地震局应急信息服务相关技术系统',
        '99': '其他'
    },
    '2': {
        '00': '互联网感知',
        '01': '通信网感知',
        '02': '舆情网感知',
        '03': '电力系统感知',
        '04': '交通系统感知',
        '05': '其他'
    },
    '3': {
        '00': '其他数据'
    }
}

carrier_code_map = {
    '0': '文字',
    '1': '图像',
    '2': '音频',
    '3': '视频',
    '4': '其他'
}

disaster_subcategory_map = {
    '1': {
        '01': '震情信息'
    },
    '2': {
        '01': '死亡',
        '02': '受伤',
        '03': '失踪'
    },
    '3': {
        '01': '土木',
        '02': '砖木',
        '03': '砖混',
        '04': '框架',
        '05': '其他'
    },
    '4': {
        '01': '交通',
        '02': '供水',
        '03': '输油',
        '04': '燃气',
        '05': '电力',
        '06': '通信',
        '07': '水利'
    },
    '5': {
        '01': '崩塌',
        '02': '滑坡',
        '03': '泥石流',
        '04': '岩溶塌陷',
        '05': '地裂缝',
        '06': '地面沉降',
        '07': '其他（沙土液化、火灾、毒气泄露、爆炸、环境污染、瘟疫、海啸等）'
    }
}
disaster_category_map={
    '1':'震情',
    '2':'人员伤亡及失踪',
    '3':'房屋破坏',
    '4':'生命线工程灾情',
    '5':'次生灾害'
}
disaster_indicator_map = {
    '1': {
        '001': '地理位置',
        '002': '时间',
        '003': '震级',
        '004': '震源烈度',
        '005': '烈度'
    },
    '2': {
        '001': '受灾人数',
        '002': '受灾程度',
    },
    '3': {
        '001': '一般损坏面积',
        '002': '严重损坏面积',
        '003': '受灾程度'
    },
    '4': {
        '001': '受灾设施数',
        '002': '受灾范围',
        '003': '受灾程度'
    },
    '5': {
        '001': '灾害损失',
        '002': '灾害范围',
        '003': '受灾程度',
        }
}
def decode_integrated_code(code,file_path):
    if len(code) != 36:
        raise ValueError("编码长度不正确，应为36位")

    # 解析震情码
    geographic_info = code[:12]
    area_info = get_area_info(geographic_info)

    event_time = code[12:26]
    event_time = datetime.strptime(event_time, '%Y%m%d%H%M%S')

    # 解析来源码
    source_category = code[26]
    source_subcategory = code[27:29]
    source = source_code_map.get(source_category, {}).get(source_subcategory, '未知')
    print(f'source:{source}')
    # 解析载体码
    carrier = carrier_code_map.get(code[29], '未知')
    print(f'carrier:{carrier}')
    # 解析灾情码
    disaster_category = disaster_category_map[code[30]]
    print(f'disaster_category:{disaster_category}')
    disaster_subcategory = disaster_subcategory_map[code[30]][code[31:33]]
    print(f'disaster_subcategory:{disaster_subcategory}')
    disaster_indicator =  disaster_indicator_map[code[30]][code[33:36]]
    print(f'disaster_indicator:{disaster_indicator}')
    #disaster = disaster_code_map.get(disaster_category, {}).get(disaster_subcategory, '未知')

    disaster_data = DisasterData(
        id=code,
        province=area_info.get('province', {}).get('name', ''),
        city=area_info.get('city', {}).get('name', ''),
        town=area_info.get('county', {}).get('name', ''),
        street=area_info.get('street', {}).get('name', ''),
        village=area_info.get('committee', {}).get('name', ''),
        disaster_category=disaster_category,
        disaster_subcategory=disaster_subcategory,
        disaster_indicator=disaster_indicator,
        source=source,
        carrier=carrier,
        timestamp=event_time,
        expiry_date=event_time,  # 这里可以根据需要设置实际的过期时间
        data_path=file_path
    )

    return disaster_data

# # 示例使用
# if __name__ == "__main__":
#     with app.app_context():
#         code = "632626200206202105220204001010302001"
#         decoded_info = decode_integrated_code(code)
#         db.session.add(decoded_info)
#         db.session.commit()
#         print(decoded_info)
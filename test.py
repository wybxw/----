import os
import unittest
from main import app, db
from models import DisasterData

class DataAccessAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # 创建数据库表
        with app.app_context():
            db.create_all()

        # 确保上传文件夹存在
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

    def tearDown(self):
        # 删除数据库表
        with app.app_context():
            db.session.remove()
            db.drop_all()

        # 清理上传文件夹
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_data_access(self):
        # 模拟文件上传
        data = {
            'id': '110101001001202105220204001010302001',
            'file': (open('path/to/your/testfile.txt', 'rb'), 'testfile.txt')
        }
        response = self.app.post('/data_access', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertIn('数据接入成功', response.get_data(as_text=True))

        # 检查数据库记录
        with app.app_context():
            disaster_data = DisasterData.query.filter_by(file_path='uploads/testfile.txt').first()
            self.assertIsNotNone(disaster_data)

if __name__ == '__main__':
    unittest.main()
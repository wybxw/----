from datetime import datetime
import pytz
from extensions import db,bcrypt
import uuid
def get_utc8_time():
    utc_time = datetime.utcnow()
    utc8_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
    return utc8_time

class DataSources(db.Model):
    __tablename__ = 'data_sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<DataSources {self.name}>'

class DisasterData(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    town = db.Column(db.String(50))
    village = db.Column(db.String(50))
    disaster_category = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, default=get_utc8_time)
    update_date = db.Column(db.DateTime, onupdate=get_utc8_time)
    uploader_id = db.Column(db.Integer)
    source_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    street = db.Column(db.String(50))
    source = db.Column(db.String(50))
    carrier = db.Column(db.String(50))
    disaster_subcategory = db.Column(db.String(50))
    disaster_indicator = db.Column(db.String(50))
    data_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'province': self.province,
            'city': self.city,
            'town': self.town,
            'village': self.village,
            'disaster_category': self.disaster_category,
            'upload_date': self.upload_date,
            'update_date': self.update_date,
            'uploader_id': self.uploader_id,
            'source_id': self.source_id,
            'timestamp': self.timestamp,
            'expiry_date': self.expiry_date,
            'street': self.street,
            'source': self.source,
            'carrier': self.carrier,
            'disaster_subcategory': self.disaster_subcategory,
            'disaster_indicator': self.disaster_indicator,
            'data_path': self.data_path
        }
class ArchivedData(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    town = db.Column(db.String(50))
    village = db.Column(db.String(50))
    disaster_category = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, default=get_utc8_time)
    update_date = db.Column(db.DateTime, onupdate=get_utc8_time)
    uploader_id = db.Column(db.Integer)
    source_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    street = db.Column(db.String(50))
    source = db.Column(db.String(50))
    carrier = db.Column(db.String(50))
    disaster_subcategory = db.Column(db.String(50))
    disaster_indicator = db.Column(db.String(50))
    data_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'province': self.province,
            'city': self.city,
            'town': self.town,
            'village': self.village,
            'disaster_category': self.disaster_category,
            'upload_date': self.upload_date,
            'update_date': self.update_date,
            'uploader_id': self.uploader_id,
            'source_id': self.source_id,
            'timestamp': self.timestamp,
            'expiry_date': self.expiry_date,
            'street': self.street,
            'source': self.source,
            'carrier': self.carrier,
            'disaster_subcategory': self.disaster_subcategory,
            'disaster_indicator': self.disaster_indicator,
            'data_path': self.data_path
        }
    
    
class User(db.Model):
    id = db.Column(db.String(255), primary_key=True,default=uuid.uuid4())
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=get_utc8_time)
    details = db.Column(db.Text)

    def __repr__(self):
        return f'<Log {self.action} by User {self.user_id}>'

class AreaCode2024(db.Model):
    __tablename__ = 'area_code_2024'
    code = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), nullable=False, default='')
    level = db.Column(db.SmallInteger, nullable=False)
    pcode = db.Column(db.BigInteger, default=None)
    category = db.Column(db.Integer, default=None)

    def __repr__(self):
        return f'<AreaCode2024 {self.code} - {self.name}>'
# 代码生成时间: 2025-09-22 23:58:18
from bottle import route, run, request, response
from bottle.ext import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_CONFIG = 'sqlite:///sql_injection_prevention.db'

# 初始化数据库连接
sqlalchemy_plugin = sqlalchemy.Plugin(sa, DATABASE_CONFIG)

# 数据库模型
class User:
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), nullable=False)
    password = sa.Column(sa.String(50), nullable=False)

# 创建数据库表
engine = sa.create_engine(DATABASE_CONFIG)
Base = sa.ext.declarative.declarative_base()
Base.metadata.create_all(engine)

# 创建会话用于数据库操作
Session = sessionmaker(bind=engine)
session = Session()

# 路由：注册用户
@route('/register', method='POST')
def register_user():
    try:
        # 获取请求数据
        username = request.forms.get('username')
        password = request.forms.get('password')

        # 校验数据
        if not username or not password:
            response.status = 400
            return {'error': 'Username and password are required'}

        # 防止SQL注入，使用参数化查询
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            response.status = 409
            return {'error': 'User already exists'}

        # 添加新用户
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()

        return {'message': 'User registered successfully'}

    except Exception as e:
        # 错误处理
        response.status = 500
        return {'error': str(e)}

# 路由：查询用户
@route('/user/<username>', method='GET')
def get_user(username):
    try:
        # 使用参数化查询防止SQL注入
        user = session.query(User).filter_by(username=username).first()
        if user:
            return {'username': user.username, 'id': user.id}
        else:
            response.status = 404
            return {'error': 'User not found'}

    except Exception as e:
        # 错误处理
        response.status = 500
        return {'error': str(e)}

# 启动服务
run(host='localhost', port=8080, debug=True)

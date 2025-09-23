# 代码生成时间: 2025-09-23 11:28:04
#!/usr/bin/env python

# sql_injection_prevention.py

from bottle import route, run, request, response
import sqlite3

# 数据库配置
DATABASE = 'example.db'

# 错误处理中间件
def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return 'Database error: ' + str(e), 500
    return wrapper

# 安全查询函数，使用参数化查询防止SQL注入
@error_handling
def safe_query(sql, params):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 主页路由，展示防止SQL注入的表单
@route('/')
def index():
    return 'Welcome to SQL Injection Prevention App!'

# 用户提交表单，防止SQL注入
@route('/submit', method='POST')
def submit():
    # 获取用户输入
    user_input = request.forms.get('input')
    # 检查输入是否为空
    if not user_input:
        return 'Input cannot be empty', 400
    
    # 使用参数化查询防止SQL注入
    sql = 'SELECT * FROM users WHERE username=?'
    results = safe_query(sql, (user_input,))
    
    # 将查询结果显示为JSON响应
    response.content_type = 'application/json'
    return {'results': [dict(row) for row in results]}

# 运行Bottle服务器
run(host='localhost', port=8080)

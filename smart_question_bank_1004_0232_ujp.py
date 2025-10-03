# 代码生成时间: 2025-10-04 02:32:24
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能题库系统
提供题目添加、查询和删除功能。
"""

from bottle import Bottle, request, run, template, error
import json

# 定义一个全局变量存储题库数据
question_bank = []
# FIXME: 处理边界情况

# 初始化 Bottle 应用
app = Bottle()

# 定义路由，添加题目
@app.route('/add_question', method='POST')
def add_question():
# TODO: 优化性能
    try:
        # 获取 JSON 数据
        data = request.json
        # 检查必要的字段是否存在
# FIXME: 处理边界情况
        if 'question' not in data or 'options' not in data or 'answer' not in data:
            return template("Question data is incomplete.")
# 改进用户体验
        # 添加题目到题库
        question_bank.append(data)
        return {"status": "success", "message": "Question added to the bank."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 定义路由，查询题目
@app.route('/query_question', method='GET')
def query_question():
    try:
        # 获取查询参数
        query_param = request.query.q
        if not query_param:
            return {"status": "error", "message": "No search term provided."}
        # 根据参数查询题库
        results = [q for q in question_bank if query_param.lower() in q['question'].lower()]
        return {"status": "success", "message": "Questions found.", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 定义路由，删除题目
@app.route('/delete_question', method='DELETE')
def delete_question():
    try:
        # 获取要删除的题目 ID
        id_to_delete = request.query.id
        if not id_to_delete:
            return {"status": "error", "message": "No question ID provided."}
        # 查找并删除题目
        initial_length = len(question_bank)
        question_bank = [q for q in question_bank if q.get('id', None) != id_to_delete]
# NOTE: 重要实现细节
        if len(question_bank) == initial_length:
            return {"status": "error", "message": "Question not found."}
        return {"status": "success", "message": "Question removed from the bank."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# 增强安全性

# 运行 Bottle 应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
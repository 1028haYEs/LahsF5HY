# 代码生成时间: 2025-10-01 03:47:24
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Environment Manager."""

from bottle import Bottle, run, request, response, error
import json

# 创建 Bottle 应用实例
app = Bottle()

# 测试环境数据存储模拟
test_environments = {
    "env1": {"name": "Environment 1", "description": "Description of Environment 1"},
    "env2": {"name": "Environment 2", "description": "Description of Environment 2"},
}

# 获取所有测试环境
@app.get("/environments")
def get_environments():
    """返回所有测试环境的列表。"""
    response.content_type = 'application/json'
    return json.dumps(test_environments)

# 获取单个测试环境
@app.get("/environments/<env_id>/")
def get_environment(env_id):
    """根据环境ID返回单个测试环境的详细信息。"""
    response.content_type = 'application/json'
    try:
        return json.dumps(test_environments[env_id])
    except KeyError:
        error(404, "Environment not found.")

# 创建一个新的测试环境
@app.post("/environments/")
def create_environment():
    """创建一个新的测试环境。"""
    if not request.json:
        error(400, "No JSON data provided.")
    env_data = request.json
    env_id = env_data.get("id")
    if not env_id or env_id in test_environments:
        error(400, "Invalid ID or ID already exists.")
    test_environments[env_id] = env_data
    response.content_type = 'application/json'
    return json.dumps(test_environments[env_id])

# 更新测试环境
@app.put("/environments/<env_id>/")
def update_environment(env_id):
    """更新指定的测试环境。"""
    response.content_type = 'application/json'
    try:
        if not request.json:
            error(400, "No JSON data provided.")
        test_environments[env_id].update(request.json)
        return json.dumps(test_environments[env_id])
    except KeyError:
        error(404, "Environment not found.")

# 删除测试环境
@app.delete("/environments/<env_id>/")
def delete_environment(env_id):
    """删除指定的测试环境。"""
    try:
        del test_environments[env_id]
        return "Environment deleted."
    except KeyError:
        error(404, "Environment not found.")

# 运行 Bottle 应用
if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)
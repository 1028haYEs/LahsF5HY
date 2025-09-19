# 代码生成时间: 2025-09-19 21:55:30
from bottle import route, run, request, template
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# 定义一个简单的图表生成函数
# 该函数将接收数据，然后生成一个图表的二进制流
def generate_chart(data):
    x = data['x']
    y = data['y']
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('Interactive Chart')

    # 将图表保存到BytesIO流中
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 返回图表的Base64编码
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# 路由：接收数据并生成图表
@route('/generate_chart', method='POST')
def chart_endpoint():
    try:
        # 解析JSON请求体
        chart_data = json.loads(request.body.read())
        # 调用图表生成函数
        chart_image = generate_chart(chart_data)
        # 返回Base64编码的图表
        return {"chart": chart_image}
    except json.JSONDecodeError:
        # 如果JSON格式错误，返回错误信息
        return {"error": "Invalid JSON format"}, 400
    except KeyError:
        # 如果缺少必要的数据，返回错误信息
        return {"error": "Missing data for chart generation"}, 400
    except Exception as e:
        # 任何其他错误，返回错误信息和状态码
        return {"error": str(e)}, 500

# 路由：返回HTML页面
@route('/')
def serve_page():
    # 返回HTML模板
    return template("""<html>
<head><title>Interactive Chart Generator</title></head>
<body>
<h2>Interactive Chart Generator</h2>
<form action="/generate_chart" method="post">
    <label for="x">Data X:</label>
    <input type="text" id="x" name="x" required>
    <br>
    <label for="y">Data Y:</label>
    <input type="text" id="y" name="y" required>
    <br>
    <input type="submit" value="Generate Chart">
</form>
</body>
</html>""")

# 运行Bottle服务器
run(host='localhost', port=8080)

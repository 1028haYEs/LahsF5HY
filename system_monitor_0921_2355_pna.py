# 代码生成时间: 2025-09-21 23:55:24
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple system performance monitoring tool using the Bottle framework.
"""

import os
import psutil
from bottle import route, run, template


# Define the base URL and port for the application
BASE_URL = "http://localhost"
PORT = 8080


# Define the route for the home page
@route("/")
def home():
    """
    Home page handler that displays system information and performance metrics.
    """
    try:
        # Collect system information and performance metrics
        system_info = {
            "hostname": os.uname().nodename,
            "cpu_cores": psutil.cpu_count(),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters(),
        }
        return template("index", system_info=system_info)
    except Exception as e:
        # Handle any exceptions that occur during data collection
        return template("error\, error=str(e))


# Start the Bottle application
if __name__ == '__main__':
    run(host=BASE_URL, port=PORT)

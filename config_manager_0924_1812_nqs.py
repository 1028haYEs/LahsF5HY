# 代码生成时间: 2025-09-24 18:12:56
#!/usr/bin/env python

"""
Configuration Manager using Bottle framework.
This script serves a simple API to manage configuration files.
"""

from bottle import Bottle, run, request, response
import json
import os

# Initialize the Bottle app
app = Bottle()

# Define the directory where configuration files will be stored
CONFIG_DIR = './configs'

# Ensure the configuration directory exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Define a route to get a configuration file
@app.route('/config/<filename:path>', method='GET')
def get_config(filename):
    """
    Get a configuration file.
    :param filename: The name of the configuration file.
    :return: The content of the configuration file.
    """
    file_path = os.path.join(CONFIG_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        response.status = 404
        return json.dumps({'error': 'Config file not found'})

# Define a route to update a configuration file
@app.route('/config/<filename:path>', method='PUT')
def update_config(filename):
    """
    Update a configuration file.
    :param filename: The name of the configuration file to update.
    :return: A success message.
    """
    file_path = os.path.join(CONFIG_DIR, filename)
    if request.content_length:
        try:
            with open(file_path, 'w') as file:
                file.write(request.body.read())
            return json.dumps({'message': 'Config updated successfully'})
        except IOError:
            response.status = 500
            return json.dumps({'error': 'Failed to update config file'})
    else:
        response.status = 400
        return json.dumps({'error': 'No data provided'})

# Define a route to delete a configuration file
@app.route('/config/<filename:path>', method='DELETE')
def delete_config(filename):
    """
    Delete a configuration file.
    :param filename: The name of the configuration file to delete.
    :return: A success message or an error message.
    """
    file_path = os.path.join(CONFIG_DIR, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return json.dumps({'message': 'Config deleted successfully'})
        except OSError:
            response.status = 500
            return json.dumps({'error': 'Failed to delete config file'})
    else:
        response.status = 404
        return json.dumps({'error': 'Config file not found'})

# Run the application if this script is the main program
if __name__ == '__main__':
    run(app, host='localhost', port=8080)

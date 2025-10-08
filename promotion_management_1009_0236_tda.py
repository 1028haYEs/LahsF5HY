# 代码生成时间: 2025-10-09 02:36:26
# -*- coding: utf-8 -*-

"""
Promotion Management Application using Bottle framework.

This application is designed to handle marketing activities.
"""

from bottle import Bottle, request, response, run
import json

# Initialize the Bottle application
app = Bottle()

# In-memory storage for promotions
promotions = {}

# Route to list all promotions
@app.route('/promotions', method='GET')
def list_promotions():
    """
    Returns a list of all promotions as JSON.
    """
    response.content_type = 'application/json'
    return json.dumps(promotions)

# Route to get a specific promotion by ID
@app.route('/promotions/<promo_id:int>', method='GET')
def get_promotion(promo_id):
    """
    Returns a specific promotion by ID as JSON.
    """
    response.content_type = 'application/json'
    promotion = promotions.get(promo_id)
    if not promotion:
        response.status = 404
        return json.dumps({'error': 'Promotion not found'})
    return json.dumps(promotion)

# Route to create a new promotion
@app.route('/promotions', method='POST')
def create_promotion():
    """
    Creates a new promotion and returns the created promotion as JSON.
    """
    try:
        data = request.json
        if not data or 'name' not in data or 'discount' not in data:
            response.status = 400
            return json.dumps({'error': 'Invalid data'})

        promo_id = len(promotions) + 1
        promotions[promo_id] = data
        response.status = 201
        return json.dumps({'message': 'Promotion created', 'id': promo_id})
    except json.JSONDecodeError:
        response.status = 400
        return json.dumps({'error': 'Invalid JSON'})

# Route to update an existing promotion
@app.route('/promotions/<promo_id:int>', method='PUT')
def update_promotion(promo_id):
    """
    Updates an existing promotion and returns the updated promotion as JSON.
    """
    try:
        data = request.json
        promotion = promotions.get(promo_id)
        if not promotion:
            response.status = 404
            return json.dumps({'error': 'Promotion not found'})

        if 'name' in data:
            promotion['name'] = data['name']
        if 'discount' in data:
            promotion['discount'] = data['discount']
        return json.dumps(promotion)
    except json.JSONDecodeError:
        response.status = 400
        return json.dumps({'error': 'Invalid JSON'})

# Route to delete a promotion
@app.route('/promotions/<promo_id:int>', method='DELETE')
def delete_promotion(promo_id):
    """
    Deletes a promotion by ID and returns a success or error message as JSON.
    """
    promotion = promotions.pop(promo_id, None)
    if not promotion:
        response.status = 404
        return json.dumps({'error': 'Promotion not found'})
    return json.dumps({'message': 'Promotion deleted'})

if __name__ == '__main__':
    # Run the application on localhost port 8080
    run(app, host='localhost', port=8080)
#!/usr/bin/python3
"""
This module create a diverse task
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    Return status ok
    Returns:
        json: status
    """
    return jsonify({"status": "OK"})

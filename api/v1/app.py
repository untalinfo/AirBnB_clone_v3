#!/usr/bin/python3
"""
This module create a blueprint
"""
from flask import Flask, make_response, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    Remove the current session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    page not found handler error 404
    Returns:
        [json]: page with json file
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True, debug=True)

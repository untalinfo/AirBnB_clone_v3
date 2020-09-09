#!/usr/bin/python3
"""
This module create a blueprint
"""
from flask import Flask, make_response, jsonify, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Remove the current session
    Args:
        exception :
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
    app.run(host='0.0.0.0', port='5000',
            threaded=True, debug=True)

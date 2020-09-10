#!/usr/bin/python3
"""
new view for State objects that handles all default
RestFul API actions
"""
from flask import Flask, jsonify, Blueprint, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieves the list of all User objects """
    _users = storage.all(User)
    list_users = []
    for key, user in _users.items():
        list_users.append(user.to_dict())

    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id=None):
    """ Retrieves a User object """
    users_id = storage.get(User, user_id)
    if users_id is None:
        abort(404)

    return jsonify(users_id.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ Delete a User object """
    users_id = storage.get(User, user_id)
    if users_id is None:
        abort(404)
    storage.delete(users_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a User object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400

    req_user = request.get_json()
    new_user = User(**req_user)  # kwargs
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_users_id(user_id=None):
    """ Retrieves a User object """
    users_id = storage.get(User, user_id)
    req_user = request.get_json()
    if users_id is None:
        abort(404)
    if not req_user:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_user.items():
        if key not in ['id', 'email', 'created_at', 'update_at']:
            setattr(users_id, key, values)

    storage.save()

    return jsonify(users_id.to_dict()), 200

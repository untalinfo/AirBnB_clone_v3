#!/usr/bin/python3
"""
new view for State objects that handles all default
RestFul API actions
"""
from flask import Flask, jsonify, Blueprint, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """ Retrieves the list of all State objects """
    list_states = storage.all(State)
    list_dic_states = []
    for key, dic_state in list_states.items():
        list_dic_states.append(dic_state.to_dict())

    return jsonify(list_dic_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id=None):
    """ Retrieves a State object """
    states_id = storage.get(State, state_id)
    if states_id is None:
        abort(404)

    return jsonify(states_id.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Delete a State object """
    states_id = storage.get(State, state_id)
    if states_id is None:
        abort(404)
    storage.delete(states_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a State object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    req_state = request.get_json()
    new_state = State(**req_state)  # kwargs
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id=None):
    """ Retrieves a State object """
    states_id = storage.get(State, state_id)
    req_state = request.get_json()
    if states_id is None:
        abort(404)
    if not req_state:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_state.items():
        setattr(states_id, key, values)

    storage.save()

    return jsonify(states_id.to_dict()), 200

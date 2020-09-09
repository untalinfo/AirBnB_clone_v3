#!/usr/bin/python3
"""
new view for State objects that handles all default
RestFul API actions
"""
from flask import Flask, jsonify, Blueprint, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id=None):
    """ Retrieves the list of all cities of a State objects """
    states_id = storage.get(State, state_id)
    if states_id is None:
        abort(404)
    list_dic_cities = []
    for city in states_id.cities:
        list_dic_cities.append(city.to_dict())

    return jsonify(list_dic_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id=None):
    """ Retrieves a City object """
    cities_id = storage.get(City, city_id)
    if cities_id is None:
        abort(404)

    return jsonify(cities_id.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ Delete a City object """
    cities_id = storage.get(City, city_id)
    if cities_id is None:
        abort(404)
    storage.delete(cities_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Create a City object """
    states_id = storage.get(State, state_id)
    if states_id is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    req_state = request.get_json()
    req_state['state_id'] = state_id
    new_city = City(**req_state)  # kwargs
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities_id(city_id=None):
    """ Retrieves a City object """
    cities_id = storage.get(City, city_id)
    req_state = request.get_json()
    if cities_id is None:
        abort(404)
    if not req_state:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_state.items():
        if key not in ['id', 'state_id', 'created_at', 'update_at']:
            setattr(cities_id, key, values)

    storage.save()

    return jsonify(cities_id.to_dict()), 200

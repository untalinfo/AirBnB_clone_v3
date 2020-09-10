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
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id=None):
    """ Retrieves the list of all places of a City objects """
    cities_id = storage.get(City, city_id)
    if cities_id is None:
        abort(404)
    list_dic_places = []
    for place in cities_id.places:
        list_dic_places.append(place.to_dict())

    return jsonify(list_dic_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id(place_id=None):
    """ Retrieves a Place object """
    places_id = storage.get(Place, place_id)
    if places_id is None:
        abort(404)

    return jsonify(places_id.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ Delete a Place object """
    places_id = storage.get(Place, place_id)
    if places_id is None:
        abort(404)

    storage.delete(places_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a Place object """
    cities_id = storage.get(City, city_id)
    if cities_id is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400

    req_place = request.get_json()
    if storage.get(User, req_place['user_id']) is None:
        abort(404)
    if 'name' not in req_place:
        return jsonify({"error": "Missing name"}), 400

    req_place['city_id'] = city_id
    req_place['user_id'] = req_place['user_id']
    new_place = Place(**req_place)  # kwargs

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_id(place_id=None):
    """ Update a City object """
    cities_id = storage.get(Place, place_id)
    req_place = request.get_json()
    if places_id is None:
        abort(404)
    if not req_places:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_place.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'update_at']:
            setattr(places_id, key, values)

    storage.save()

    return jsonify(places_id.to_dict()), 200

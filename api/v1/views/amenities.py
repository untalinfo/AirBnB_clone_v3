#!/usr/bin/python3
"""
New view for Amenity objects that handles all default
RestFul API actions
"""
from flask import Flask, jsonify, Blueprint, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieves the list of all Amenity objects """
    list_amenities = storage.all(Amenity)
    list_dic_amenities = []
    for key, dic_state in list_amenities.items():
        list_dic_amenities.append(dic_state.to_dict())

    return jsonify(list_dic_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id=None):
    """ Retrieves a Amenity object """
    amenities_id = storage.get(Amenity, amenity_id)
    if amenities_id is None:
        abort(404)

    return jsonify(amenities_id.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Delete a Amenity object """
    amenities_id = storage.get(Amenity, amenity_id)
    if amenities_id is None:
        abort(404)
    storage.delete(amenities_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenitiy():
    """ Create a Amenity object """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    req_amenity = request.get_json()
    new_amenity = Amenity(**req_amenity)  # kwargs
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_id(amenity_id=None):
    """ Retrieves a Amenity object """
    amenities_id = storage.get(Amenity, amenity_id)
    req_amenity = request.get_json()
    if amenities_id is None:
        abort(404)
    if not req_amenity:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_amenity.items():
        setattr(amenities_id, key, values)

    storage.save()

    return jsonify(amenities_id.to_dict()), 200

#!/usr/bin/python3
"""
new view for Review object that handles all default
RestFul API actions
"""
from flask import Flask, jsonify, Blueprint, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_riviews(place_id=None):
    """ Retrieves the list of all reviews of a Place objects """
    places_id = storage.get(Place, place_id)
    if states_id is None:
        abort(404)
    list_dic_reviews = []
    for review in places_id.reviews:
        list_dic_reviwes.append(review.to_dict())

    return jsonify(list_dic_riviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def riviews_id(review_id=None):
    """ Retrieves a Review object """
    reviews_id = storage.get(Review, review_id)
    if reviews_id is None:
        abort(404)

    return jsonify(reviews_id.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Delete a Review object """
    reviews_id = storage.get(Review, review_id)
    if reviews_id is None:
        abort(404)
    storage.delete(reviews_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Create a Review object """
    places_id = storage.get(Place, place_id)
    if states_id is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in request.get_json():
        return jsonify({"error": "Missing text"}), 400

    req_place = request.get_json()
    req_place['place_id'] = place_id
    new_review = Review(**req_state)  # kwargs
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews_id(review_id=None):
    """ Retrieves a Review object """
    reviews_id = storage.get(Review, review_id)
    req_review = request.get_json()
    if reviews_id is None:
        abort(404)
    if not req_review:
        return jsonify({"error": "Not a JSON"}), 400

    for key, values in req_review.items():
        if key not in ['id', 'user_id', 'place_id' 'created_at', 'update_at']:
            setattr(reviews_id, key, values)

    storage.save()

    return jsonify(reviews_id.to_dict()), 200

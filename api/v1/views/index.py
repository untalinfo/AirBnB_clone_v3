#!/usr/bin/python3
""" Module to retrives an object """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Return status ok
    Returns:
        json: status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def cls_stats():
    """
    Method that retrieves the number of each objects by type
    Ex:
    {
      "amenities": 47,
      "cities": 36,
      "places": 154,
      "reviews": 718,
      "states": 27,
      "users": 31
    }
    list_cls = list(set(cls.split(".")[0] for cls in storage.all()))
    for cls in list_cls:
        print(cls)
        print(storage.count(cls))
    for cls in list_cls:
        dict_count.update({cls: storage.count(cls)})
    """
    dict_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(dict_count)

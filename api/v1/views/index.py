#!/usr/bin/python3
"""Routing for views"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

all_obj = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def show_status():
    """Shows the status of the API
    Returns:
    A JSON string of the status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def show_stats():
    """returns the count of all objects"""
    for key, value in all_obj.items():
        all_obj[key] = storage.count(value)
    return jsonify(all_obj)

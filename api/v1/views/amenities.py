#!/usr/bin/python3
"""create a new view for City objects that handles all default
RESTFul API actions
"""
from models import storage
from flask import request, abort, make_response, jsonify
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """retrives all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_an_amenity(amenity_id):
    """retrieves an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create an amenity"""
    if request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in request.json:
        return make_response(jsonify('Missing name'), 400)
    content = request.get_json(silent=True)
    amenity = Amenity(**content)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_an_amenity(amenity_id):
    """updates an amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    for key, value in request.json.items():
        setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)

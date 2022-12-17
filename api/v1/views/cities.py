#!/usr/bin/python3
"""create a new view for City objects that handles all default
RESTFul API actions
"""
from models import storage
from flask import request, abort, make_response, jsonify
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_in_state(state_id):
    """retrives all cities in a state"""

    citiesl = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        citiesl.append(city.to_dict())
    return jsonify(citiesl)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """retrieves a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in request.json:
        return make_response(jsonify('Missing name'), 400)
    content = request.get_json(silent=True)
    city = City(**content)
    setattr(city, 'state_id', state_id)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id):
    """updates a city"""

    ignore = ['id', 'updated_at', 'created_at', 'state_id']
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    for key, value in request.json.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

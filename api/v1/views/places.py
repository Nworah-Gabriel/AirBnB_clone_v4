#!/usr/bin/python3
"""API routes for Places"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City
       Parameters:
           city_id (str):
       Returns:
           A list of JSON dictionaries of all places in a city
    """
    city = storage.get(City, city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object.
       Parameters:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object.
       Parameters:
           place_id (str): place uuid
       Returns:
           Empty JSON dictionary if successful otherwise 404 error
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place.
       Parameters:
           city_id (str): city uuid
       Returns:
           JSON dictionary of place if successful
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify('Not a JSON'), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify('Missing user_id'), 400)
    user_id = request.json.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return make_response(jsonify('Missing name'), 400)
    content = request.get_json(silent=True)
    place = Place(**content)
    place.save()
    setattr(place, 'city_id', city_id)
    return make_response(place.to_json(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object.
       Parameters:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place if successful
    """
    ignore = ['id', 'updated_at', 'created_at', 'user_id', 'city_id']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.json(silent=True)
    if type(content) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in content.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_json()), 200)


@app_views.route("/places_search/", methods=["POST"], strict_slashes=False)
def search_places():
    places_list = []
    place_dicts = []
    cities_list = []
    removal_list = []
    empty = True
    content = request.get_json(silent=True)

    if type(content) is dict:
        for key, value in content.items():
            if len(content[key]) > 0:
                empty = False

        if len(content) == 0 or empty is True:
            places = storage.all("Place").values()
            for place in places:
                place_dicts.append(place.to_dict())

        if "states" in content:
            for state in content["states"]:
                state_obj = storage.get("State", state)
                if state_obj:
                    for city in state_obj.cities:
                        cities_list.append(city)

        if "cities" in content:
            for city in content["cities"]:
                city_obj = storage.get("City", city)
                if city_obj:
                    cities_list.append(city_obj)

        for city in cities_list:
            for place in city.places:
                places_list.append(place)

        if "amenities" in content:
            for place in places_list:
                for amenity in content["amenities"]:
                    amenity_obj = storage.get("Amenity", amenity)
                    if amenity_obj:
                        if amenity_obj not in place.amenities:
                            removal_list.append(place)
                            break

        for place in removal_list:
            if place in places_list:
                places_list.remove(place)

        for place in places_list:
            place_dicts.append(place.to_dict())

        return jsonify(place_dicts)

    else:
        response = jsonify({"error": "Not a JSON"})
        response.status_code = 400
        return response

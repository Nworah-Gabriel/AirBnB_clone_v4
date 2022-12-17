#!/usr/bin/python3
"""Place-Amenity API Routes"""
from models import storage
from flask import jsonify, abort
from api.v1.views import app_views

# from models.review import Review
from models.place import Place

# from models.user import User
from models.amenity import Amenity


@app_views.route(
    "/places/<place_id>/amenities/",
    methods=["GET"],
    strict_slashes=False
    )
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place.
    Parameters:
        place_id (str): the id of the place to display amenities
    Returns:
        A list of JSON dictionaries of all amenities in a 200 response
    """
    amenities_list = []
    place = storage.get(Place, place_id)
    if place:
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place.
    Parameters:
        place_id (str): the id of the place
        amenity_id (str): id of amenity to delete
    Returns:
        An empty JSON dictionary in a 200 response
        A 404 response if the id does not match
    """
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if amenity in place.amenities:
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False
)
def create_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place.
    Parameters:
        place_id (str): the id of the place
        amenity_id (str): id of the amenity
    Returns:
        A JSON dictionary of the amenity in a 201 response
        A 404 response if not match for ids
    """
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            else:
                place.amenities.append(amenity)
                storage.save()
                response = jsonify(amenity.to_dict())
                response.status_code = 201
                return response
        else:
            abort(404)
    else:
        abort(404)

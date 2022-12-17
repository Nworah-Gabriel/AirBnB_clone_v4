#!/usr/bin/python3
"""Routes for User API"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """Shows all users.
           Returns:
               A list of JSON dictionaries of all users in a 200 response
    """
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Shows a specific user based on id.
           Parameters:
               user_id [str]: the id of the user to display

           Returns:
               A JSON dictionary of the user in a 200 response
               A 404 response if the id does not match
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>/', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific user based on id.
           Parameters:
               user_id [str]: the id of the user to delete

           Returns:
               An empty JSON dictionary in a 200 response
               A 404 response if the id does not match
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user.
           Returns:
               A JSON dictionary of a new user in a 200 response
               A 400 response if missing parameters or if not valid JSON
    """
    error_message = ""
    if not request.json:
        return abort(400, {'error': 'Not a JSON'})
    content = request.get_json(silent=True)
    if "email" in content.keys() and "password" in content.keys():
        user = User(**content)
        # storage.new(user)
        # storage.save()
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        if "email" not in content.keys():
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if "password" not in content.keys():
            return make_response(jsonify({'error': 'Missing password'}), 400)


@app_views.route('/users/<user_id>/', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing user.
           Parameters:
               user_id [str]: the id of the user to update

           Returns:
               A JSON dictionary of the updated user in a 200 response
               A 400 response if not a valid JSON
               A 404 response if the id does not match
    """
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get(User, user_id)
    if user:
        content = request.get_json(silent=True)
        if isinstance(content, dict):
            for key, value in content.items():
                if key not in ignore:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict())
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)

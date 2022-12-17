#!/usr/bin/python3
"""Routes for States API"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Shows all states.
           Returns:
               A list of JSON disctionaries of all states.
    """
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Shows a specific state based on id.
           Parameters:
               state_id [str]: the id of the state to display
           Returns:
               A JSON dictionary of the state in a 200 response
               A 404 response if the id does not match
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific state.
            Parameters:
                state_id [str]: the id of the state
            Returns:
                An empty JSON dictionary in a 200 response.
                a 404 response if the id does not match.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state object
           Returns:
               A JSON dictionary of the new state in a 200 response
               A 400 response if not a valid JSON or if missing parameters
    """
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "name" in content.keys():
            state = State(**content)
            # storage.save()
            # storage.new(State)
            state.save()
            response = jsonify(state.to_dict())
            response.status_code = 201
            return response
        else:
            error_message = "Missing name"
    else:
        error_message = "Not a JSON"

    response = jsonify(error_message)
    response.status_code = 400
    return response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state object based on id
           Parameters:
               state_id [str]: the id of the state to update
           Returns:
               A JSON dictionary of the udpated state in a 200 response
               A 400 response if not a valid JSON
               A 404 response if the id does not match
    """
    ignore = ['id', 'updated_at', 'created_at']
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return make_response(jsonify('Not a JSON'), 400)
    if request.get_json is None:
        return make_response(jsonify('Not a JSON'), 400)
    update_cnt = request.get_json(silent=True)
    for key, value in update_cnt.items():
        if key not in ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())

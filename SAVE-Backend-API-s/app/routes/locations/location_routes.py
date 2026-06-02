from flask import (
    Blueprint,
    jsonify
)

location_bp = Blueprint(
    'locations',
    __name__
)

@location_bp.route(
    '/api/v1/locations',
    methods=['GET']
)
def list_locations():

    return jsonify({
        'status': 'success',
        'message': 'Locations endpoint'
    })
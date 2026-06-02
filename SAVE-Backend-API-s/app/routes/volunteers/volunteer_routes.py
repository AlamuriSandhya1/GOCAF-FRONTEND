from flask import (
    Blueprint,
    jsonify
)

volunteer_bp = Blueprint(
    'volunteers',
    __name__
)

@volunteer_bp.route(
    '/api/v1/volunteers',
    methods=['GET']
)
def list_volunteers():

    return jsonify({
        'status': 'success',
        'message': 'Volunteers endpoint'
    })
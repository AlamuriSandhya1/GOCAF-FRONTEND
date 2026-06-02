from flask import (
    Blueprint,
    jsonify
)

rescuer_bp = Blueprint(
    'rescuers',
    __name__
)

@rescuer_bp.route(
    '/api/v1/rescuers',
    methods=['GET']
)
def list_rescuers():

    return jsonify({
        'status': 'success',
        'message': 'Rescuers endpoint'
    })
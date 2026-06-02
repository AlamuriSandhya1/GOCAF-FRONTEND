from flask import (
    Blueprint,
    jsonify
)

caretaker_bp = Blueprint(
    'caretakers',
    __name__
)

@caretaker_bp.route(
    '/api/v1/caretakers',
    methods=['GET']
)
def list_caretakers():

    return jsonify({
        'status': 'success',
        'message': 'Caretakers endpoint'
    })
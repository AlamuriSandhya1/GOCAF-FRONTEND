from flask import (
    Blueprint,
    jsonify
)

feeder_bp = Blueprint(
    'feeders',
    __name__
)

@feeder_bp.route(
    '/api/v1/feeders',
    methods=['GET']
)
def list_feeders():

    return jsonify({
        'status': 'success',
        'message': 'Feeders endpoint'
    })
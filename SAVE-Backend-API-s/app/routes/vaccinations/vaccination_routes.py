from flask import (
    Blueprint,
    jsonify
)

vaccination_bp = Blueprint(
    'vaccinations',
    __name__
)

@vaccination_bp.route(
    '/api/v1/vaccinations/<scan_code>',
    methods=['GET']
)
def vaccination_history(scan_code):

    return jsonify({
        'status': 'success',
        'scan_code': scan_code,
        'message': 'Vaccination history endpoint'
    })
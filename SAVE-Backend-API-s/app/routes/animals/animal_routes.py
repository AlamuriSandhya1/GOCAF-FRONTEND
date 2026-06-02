from flask import (
    Blueprint,
    jsonify,
    request
)

from app.services.animal_service import (
    get_animal,
    update_animal,
    fetch_medical_history
)

animal_bp = Blueprint(
    'animals',
    __name__,
    url_prefix='/api/v1/animals'
)


# ======================================
# HEALTH CHECK
# ======================================

@animal_bp.route(
    '/health',
    methods=['GET']
)
def animal_health():

    return jsonify({

        'status': 'success',

        'message': 'Animals API Running'
    })


# ======================================
# GET SINGLE ANIMAL
# ======================================

@animal_bp.route(
    '/<scan_code>',
    methods=['GET']
)
def get_single_animal(scan_code):

    animal = get_animal(
        scan_code
    )

    if not animal:

        return jsonify({

            'status': 'error',

            'message': 'Animal Not Found'
        }), 404

    medical_history = fetch_medical_history(
        animal['internal_id']
    )

    return jsonify({

        'status': 'success',

        'animal': animal,

        'medical_history': medical_history
    })


# ======================================
# UPDATE ANIMAL MASTER
# ======================================

@animal_bp.route(
    '/<scan_code>',
    methods=['PUT']
)
def update_single_animal(scan_code):

    data = request.json

    animal = get_animal(
        scan_code
    )

    if not animal:

        return jsonify({

            'status': 'error',

            'message': 'Animal Not Found'
        }), 404

    update_animal(
        scan_code,
        data
    )

    updated_animal = get_animal(
        scan_code
    )

    return jsonify({

        'status': 'success',

        'message': 'Animal Updated Successfully',

        'animal': updated_animal
    })


# ======================================
# GET MEDICAL HISTORY
# ======================================

@animal_bp.route(
    '/<scan_code>/medical-history',
    methods=['GET']
)
def get_animal_medical_history(scan_code):

    animal = get_animal(
        scan_code
    )

    if not animal:

        return jsonify({

            'status': 'error',

            'message': 'Animal Not Found'
        }), 404

    medical_history = fetch_medical_history(
        animal['internal_id']
    )

    return jsonify({

        'status': 'success',

        'scan_code': scan_code,

        'medical_history': medical_history
    })


# ======================================
# API INFO
# ======================================

@animal_bp.route(
    '/',
    methods=['GET']
)
def animal_api_info():

    return jsonify({

        'status': 'success',

        'service': 'GOCAF SAVE Animals API',

        'version': 'v1',

        'routes': {

            'health': '/api/v1/animals/health',

            'get_animal':
                '/api/v1/animals/<scan_code>',

            'update_animal':
                '/api/v1/animals/<scan_code>',

            'medical_history':
                '/api/v1/animals/<scan_code>/medical-history'
        }
    })

################# above working code but encode ###########################

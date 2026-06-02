from flask import Flask

from app.routes.public_routes import (
    public_bp
)


from app.routes.admin_routes import (
    admin_bp
)

from app.routes.animals.animal_routes import (
    animal_bp
)

from app.routes.vaccinations.vaccination_routes import (
    vaccination_bp
)

from app.routes.caretakers.caretaker_routes import (
    caretaker_bp
)

from app.routes.locations.location_routes import (
    location_bp
)

from app.routes.feeders.feeder_routes import (
    feeder_bp
)

from app.routes.rescuers.rescuer_routes import (
    rescuer_bp
)

from app.routes.volunteers.volunteer_routes import (
    volunteer_bp
)


def create_app():

    app = Flask(__name__)
    app.secret_key = 'gocaf-save-secret'
    # =========================
    # ADMIN ROUTES
    # =========================

    app.register_blueprint(
        admin_bp
    )

    # =========================
    # API ROUTES
    # =========================
    ## Register animal from HTML 
    app.register_blueprint(
    public_bp
    )


    app.register_blueprint(
        animal_bp
    )

    app.register_blueprint(
        vaccination_bp
    )

    app.register_blueprint(
        caretaker_bp
    )

    app.register_blueprint(
        location_bp
    )

    app.register_blueprint(
        feeder_bp
    )

    app.register_blueprint(
        rescuer_bp
    )

    app.register_blueprint(
        volunteer_bp
    )

    # =========================
    # HEALTH CHECK
    # =========================

    @app.route('/health')

    def health():

        return {
            'status': 'success',
            'message': 'GOCAF SAVE API Running'
        }

    return app
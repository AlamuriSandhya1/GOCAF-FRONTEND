import os

from werkzeug.utils import secure_filename

from flask import (

    Blueprint,
    render_template,
    request,
    flash,
    send_from_directory
)

from datetime import datetime

import random
import string

from app.services.animal_service import (
    create_animal_registration
)

from app.services.volunteer_service import (
    create_volunteer_registration
)

public_bp = Blueprint(

    'public',

    __name__
)

# ======================================
# VOLUNTEER REGISTRATION PAGE
# ======================================

@public_bp.route(
    '/volunteer-registration'
)
def volunteer_registration():

    return render_template(
        'volunteer-register/volunteer_register.html'
    )

@public_bp.route("/")
def home():
    return render_template("index.html")

@public_bp.route("/save")
def save():
    return render_template("save.html")


# @public_bp.route("/care")
# def care():
#     return render_template("care.html")


# @public_bp.route("/saveplus")
# def saveplus():
#     return render_template("saveplus.html")


# @public_bp.route("/careplus")
# def careplus():
#     return render_template("careplus.html")
# ======================================
# VOLUNTEER REGISTRATION
# ======================================

@public_bp.route(
    '/register-volunteer',
    methods=['POST']
)
def register_volunteer():

    form_data = request.form.to_dict()

    # ==================================
    # TIMESTAMP
    # ==================================

    form_data['Timestamp'] = (
        datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )
    )

    # ==================================
    # GENERATE INTERNAL VOLUNTEER ID
    # ==================================

    internal_random = ''.join(

        random.choices(

            string.ascii_uppercase +
            string.digits,

            k=8
        )
    )

    volunteer_internal_id = (
        f'GCFVOL-{internal_random}'
    )

    form_data[
        'volunteer_internal_id'
    ] = volunteer_internal_id

    # ==================================
    # GENERATE PUBLIC VOLUNTEER ID
    # ==================================

    public_random = ''.join(

        random.choices(

            string.digits,

            k=6
        )
    )

    volunteer_public_id = (
        f'GOCAFVOL#{public_random}'
    )

    form_data[
        'volunteer_id'
    ] = volunteer_public_id

    # ==================================
    # STATUS
    # ==================================

    form_data[
        'registration_status'
    ] = 'pending'

    # ==================================
    # VOLUNTEER ID UPLOAD
    # ==================================

    volunteer_id_file = request.files.get(
        'Volunteer ID Upload'
    )

    volunteer_id_path = ''

    if volunteer_id_file:

        filename = secure_filename(
            volunteer_id_file.filename
        )

        timestamp = datetime.now().strftime(
            '%Y%m%d%H%M%S'
        )

        filename = (
            f'{timestamp}_{filename}'
        )

        upload_folder = os.path.join(

            os.getcwd(),

            'uploads',

            'volunteer_ids'
        )

        if not os.path.exists(upload_folder):

            os.makedirs(upload_folder)

        full_path = os.path.join(

            upload_folder,

            filename
        )

        volunteer_id_file.save(
            full_path
        )

        volunteer_id_path = (
            f'/uploads/volunteer_ids/{filename}'
        )

    form_data[
        'Volunteer ID Upload'
    ] = volunteer_id_path

    # ==================================
    # SAVE TO GOOGLE SHEET
    # ==================================

    create_volunteer_registration(
        form_data
    )

    # ==================================
    # SUCCESS PAGE
    # ==================================

    return render_template(

        'volunteer-register/volunteer_success.html',

        volunteer_id=volunteer_public_id

    )


# ======================================
# PUBLIC ANIMAL REGISTRATION PAGE
# ======================================

@public_bp.route(
    '/saveregistration'
)
def save_registration():

    return render_template(
        'animal-register/animal_register.html'
    )


# ======================================
# GENERATE INTERNAL ANIMAL ID
# ======================================

def generate_internal_id():

    random_part = ''.join(

        random.choices(

            string.ascii_uppercase +
            string.digits,

            k=8
        )
    )

    return f'ANMDG-{random_part}'


# ======================================
# REGISTER ANIMAL
# ======================================

@public_bp.route(
    '/register-animal',
    methods=['POST']
)
def register_animal():

    form_data = request.form.to_dict()

    # ==============================
    # ANIMAL PHOTO UPLOAD
    # ==============================

    photo = request.files.get(
        'animal_photo'
    )

    photo_path = ''

    if photo:

        filename = secure_filename(
            photo.filename
        )

        timestamp = datetime.now().strftime(
            '%Y%m%d%H%M%S'
        )

        filename = f"{timestamp}_{filename}"

        upload_folder = (
            'uploads/animals'
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        full_path = os.path.join(
            upload_folder,
            filename
        )

        photo.save(
            full_path
        )

        photo_path = (
            f'/uploads/animals/{filename}'
        )

    form_data['Upload Animal Photos'] = (
        photo_path
    )

    # ==============================
    # CARETAKER ID UPLOAD
    # ==============================

    caretaker_id = request.files.get(
        'caretaker_id_proof'
    )

    caretaker_id_path = ''

    if caretaker_id:

        caretaker_filename = secure_filename(
            caretaker_id.filename
        )

        timestamp = datetime.now().strftime(
            '%Y%m%d%H%M%S'
        )

        caretaker_filename = (
            f"{timestamp}_{caretaker_filename}"
        )

        caretaker_upload_folder = (
            'uploads/caretaker_ids'
        )

        os.makedirs(
            caretaker_upload_folder,
            exist_ok=True
        )

        caretaker_full_path = os.path.join(

            caretaker_upload_folder,

            caretaker_filename
        )

        caretaker_id.save(
            caretaker_full_path
        )

        caretaker_id_path = (
            f'/uploads/caretaker_ids/{caretaker_filename}'
        )

    form_data['ID Proof Upload'] = (
        caretaker_id_path
    )

    # ==============================
    # TIMESTAMP
    # ==============================

    form_data['Timestamp'] = (
        datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )
    )

    # ==============================
    # INTERNAL ID
    # ==============================

    internal_id = (
        generate_internal_id()
    )

    form_data['internal_id'] = (
        internal_id
    )

    # ==============================
    # SAVE IDS
    # ==============================

    form_data['save_id'] = ''

    form_data['short_save_id'] = ''

    # ==============================
    # STATUS
    # ==============================

    form_data['registration_status'] = (
        'pending'
    )

    # ==============================
    # SAVE TO SHEET
    # ==============================

    create_animal_registration(
        form_data
    )

    flash(
        'Registration Submitted Successfully',
        'success'
    )

    # ==============================
    # SUCCESS PAGE
    # ==============================

    return render_template(

        'animal-register/registration_success.html'
    )


# ======================================
# SERVE ANIMAL IMAGES
# ======================================

@public_bp.route(
    '/uploads/animals/<filename>'
)
def uploaded_animal_image(
    filename
):

    return send_from_directory(

        'uploads/animals',

        filename
    )


# ======================================
# SERVE CARETAKER IDS
# ======================================

@public_bp.route(
    '/uploads/caretaker_ids/<filename>'
)
def uploaded_caretaker_id(
    filename
):

    return send_from_directory(

        'uploads/caretaker_ids',

        filename
    )


# ======================================
# SERVE VOLUNTEER IDS
# ======================================

@public_bp.route(
    '/uploads/volunteer_ids/<filename>'
)
def uploaded_volunteer_id(
    filename
):

    return send_from_directory(

        'uploads/volunteer_ids',

        filename
    )
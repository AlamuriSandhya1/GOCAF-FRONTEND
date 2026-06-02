from flask import (

    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from datetime import datetime

# animal function imports
from app.services.animal_service import (

    get_animal,
    update_animal,
    create_medical_record,
    fetch_medical_history
)

# Volunteer function imports
from app.services.volunteer_service import (
    get_all_volunteers,
    search_volunteer
)

#admin blueprint
admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)

# ======================================
# ADMIN LOGIN PAGE
# ======================================

@admin_bp.route(
    '/login'
)
def admin_login():

    return render_template(
        'admin/admin_login.html'
    )

# ======================================
# VOLUNTEER ADMIN DASHBOARD
# ======================================

@admin_bp.route(
    #'/admin/volunteers'
    '/volunteers'
)
def admin_volunteers():

    volunteers = get_all_volunteers()

    return render_template(
        'admin/volunteer_admin.html',
        volunteers=volunteers
    )


# ======================================
# SEARCH VOLUNTEER
# ======================================

@admin_bp.route(
    '/search-volunteer'
)
def search_volunteer_admin():

    query = request.args.get(
        'query'
    )

    volunteers = search_volunteer(
        query
    )

    return render_template(
        'admin/volunteer_admin.html',
        volunteers=volunteers
    )

# ======================================
# ADMIN HOME - Animal reg save
# ======================================

@admin_bp.route('/')

def admin_home():

    return render_template(
        'admin/admin.html'
    )


# ======================================
# SEARCH ANIMAL
# ======================================

@admin_bp.route(

    '/search',

    methods=['POST']
)

def admin_search():

    scan_code = request.form.get(
        'scan_code'
    )

    animal = get_animal(
        scan_code
    )

    if not animal:

        return render_template(

            'admin/admin.html',

            error='Animal Not Found'
        )

    medical_history = fetch_medical_history(

        animal['internal_id']
    )

    return render_template(

        'admin/admin.html',

        animal=animal,

        medical_history=medical_history
    )


# ======================================
# UPDATE ANIMAL
# ======================================

@admin_bp.route(

    '/update',

    methods=['POST']
)

def admin_update():

    form_data = request.form.to_dict()

    form_data['Updated By'] = (
        'admin@gocaf.global'
    )

    form_data['Updated At'] = (

        datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        )
    )

    scan_code = form_data.get(
        'short_save_id'
    )

    internal_id = form_data.get(
        'internal_id'
    )

    # ==================================
    # UPDATE MASTER RECORD
    # ==================================

    update_animal(

        scan_code,

        form_data
    )

    # ==================================
    # CREATE MEDICAL RECORD
    # ==================================

    animal = {

        'internal_id': internal_id,

        'short_save_id': scan_code
    }

    create_medical_record(

        animal,

        form_data
    )

    # ==================================
    # FETCH UPDATED DATA
    # ==================================

    updated_animal = get_animal(
        scan_code
    )

    medical_history = fetch_medical_history(
        internal_id
    )

    flash(
    'Animal Updated Successfully',
    'success'
)

    return redirect(
        url_for(
            'admin.admin_home'
        )
    )


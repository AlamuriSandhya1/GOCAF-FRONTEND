import gspread
import random
import string
import uuid

from oauth2client.service_account import (
    ServiceAccountCredentials
)

from datetime import datetime


# ======================================
# GOOGLE SHEETS CONNECTION
# ======================================

scope = [

    'https://spreadsheets.google.com/feeds',

    'https://www.googleapis.com/auth/drive'
]

credentials = (
    ServiceAccountCredentials
    .from_json_keyfile_name(
        'credentials.json',
        scope
    )
)

client = (
    gspread.authorize(
        credentials
    )
)

spreadsheet = client.open_by_key(
    '1RUprnj317RdjZHrBPdMRgYW2JSf3kzcvGUGsIngJEJo'
)

animals_master_sheet = (
    spreadsheet.worksheet(
        'animals_master'
    )
)

medical_sheet = (
    spreadsheet.worksheet(
        'medical_records'
    )
)


# ======================================
# GENERATE INTERNAL ID
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
# CREATE REGISTRATION
# ======================================

def create_animal_registration(
    form_data
):

    headers = (
        animals_master_sheet
        .row_values(1)
    )

    # ==============================
    # SYSTEM GENERATED FIELDS
    # ==============================

    form_data['Timestamp'] = (
        datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )
    )

    form_data['internal_id'] = (
        generate_internal_id()
    )

    # Assigned Later By Admin

    form_data['save_id'] = ''

    form_data['short_save_id'] = ''

    form_data['registration_status'] = (
        'pending'
    )

    # ==============================
    # BUILD ROW
    # ==============================

    row = []

    for header in headers:

        row.append(

            form_data.get(
                header,
                ''
            )
        )

    # ==============================
    # WRITE TO SHEET
    # ==============================

    animals_master_sheet.append_row(
        row
    )


# ======================================
# GET ANIMAL
# ======================================

def get_animal(scan_code):

    records = (
        animals_master_sheet
        .get_all_records()
    )

    for animal in records:

        if (

            animal.get(
                'short_save_id'
            ) == scan_code

            or

            animal.get(
                'save_id'
            ) == scan_code
        ):

            return animal

    return None


# ======================================
# UPDATE ANIMAL
# ======================================

def update_animal(
    scan_code,
    form_data
):

    records = (
        animals_master_sheet
        .get_all_records()
    )

    headers = (
        animals_master_sheet
        .row_values(1)
    )

    for index, animal in enumerate(
        records,
        start=2
    ):

        if (

            animal.get(
                'short_save_id'
            ) == scan_code

            or

            animal.get(
                'save_id'
            ) == scan_code
        ):

            for key, value in form_data.items():

                if key in headers:

                    column = (
                        headers.index(key) + 1
                    )

                    animals_master_sheet.update_cell(

                        index,
                        column,
                        value
                    )

            return True

    return False


# ======================================
# CREATE MEDICAL RECORD
# ======================================

def create_medical_record(
    animal,
    form_data
):

    medical_headers = (
        medical_sheet
        .row_values(1)
    )

    medical_data = {

        'medical_id':
            f"MED_{uuid.uuid4().hex[:8]}",

        'internal_id':
            animal.get(
                'internal_id',
                ''
            ),

        'short_save_id':
            animal.get(
                'short_save_id',
                ''
            ),

        'Temperature':
            form_data.get(
                'Temperature',
                ''
            ),

        'Weight':
            form_data.get(
                'Weight',
                ''
            ),

        'ARV_Status':
            form_data.get(
                'ARV_Status',
                ''
            ),

        'ARV_Date':
            form_data.get(
                'ARV_Date',
                ''
            ),

        'Booster_Status':
            form_data.get(
                'Booster_Status',
                ''
            ),

        'Booster_Date':
            form_data.get(
                'Booster_Date',
                ''
            ),

        'Deworming_Status':
            form_data.get(
                'Deworming_Status',
                ''
            ),

        'Deworming_Date':
            form_data.get(
                'Deworming_Date',
                ''
            ),

        'Medical_Condition':
            form_data.get(
                'Medical_Condition',
                ''
            ),

        'Medicines':
            form_data.get(
                'Medicines',
                ''
            ),

        'Dosage':
            form_data.get(
                'Dosage',
                ''
            ),

        'Treatment_Days':
            form_data.get(
                'Treatment_Days',
                ''
            ),

        'Vet_Name':
            form_data.get(
                'Vet_Name',
                ''
            ),

        'Next_Visit_Date':
            form_data.get(
                'Next_Visit_Date',
                ''
            ),

        'Updated_By':
            form_data.get(
                'Updated By',
                ''
            ),

        'Updated_At':
            datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
            )
    }

    row = []

    for header in medical_headers:

        row.append(

            medical_data.get(
                header,
                ''
            )
        )

    medical_sheet.append_row(
        row
    )


# ======================================
# FETCH MEDICAL HISTORY
# ======================================

def fetch_medical_history(
    internal_id
):

    records = (
        medical_sheet
        .get_all_records()
    )

    history = []

    for row in records:

        if (

            row.get(
                'internal_id'
            ) == internal_id
        ):

            history.append(
                row
            )

    return history
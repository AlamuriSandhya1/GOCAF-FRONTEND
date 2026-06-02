# this is for animal register master data - SAVE registration FORM DATA 

import uuid
import gspread

from google.oauth2.service_account import (
    Credentials
)

from config.settings import (
    SHEET_ID
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

CREDS = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(
    CREDS
)

spreadsheet = client.open_by_key(
    SHEET_ID
)

# ======================================
# MASTER SHEET
# ======================================

animal_sheet = spreadsheet.sheet1

# ======================================
# MEDICAL SHEET
# ======================================

medical_sheet = spreadsheet.worksheet(
    'medical_records'
)


# ======================================
# GET ALL ANIMALS
# ======================================

def get_all_records():

    return animal_sheet.get_all_records()


# ======================================
# UPDATE MASTER RECORD
# ======================================

def update_record(
    scan_code,
    form_data
):

    records = animal_sheet.get_all_records()

    headers = animal_sheet.row_values(1)

    for index, row in enumerate(
        records,
        start=2
    ):

        if (
            str(
                row['short_save_id']
            ).upper()
            ==
            scan_code.upper()
        ):

            for field, value in form_data.items():

                if (
                    field in headers
                    and field != 'short_save_id'
                ):

                    col_number = (
                        headers.index(field)
                        + 1
                    )

                    animal_sheet.update_cell(
                        index,
                        col_number,
                        value
                    )

            return True

    return False


# ======================================
# CREATE MEDICAL RECORD
# ======================================

def add_medical_record(
    animal,
    form_data
):

    import uuid

    medical_id = (
        f"MED_{uuid.uuid4().hex[:8]}"
    )

    row = [

        medical_id,

        animal['internal_id'],

        animal['short_save_id'],

        form_data.get(
            'Temperature',
            ''
        ),

        form_data.get(
            'Weight',
            ''
        ),

        form_data.get(
            'ARV Status',
            ''
        ),

        form_data.get(
            'ARV Date',
            ''
        ),

        form_data.get(
            'Booster Status',
            ''
        ),

        form_data.get(
            'Booster Date',
            ''
        ),

        form_data.get(
            'Deworming Status',
            ''
        ),

        form_data.get(
            'Deworming Date',
            ''
        ),

        form_data.get(
            'Medical Condition',
            ''
        ),

        form_data.get(
            'Medicines',
            ''
        ),

        form_data.get(
            'Dosage',
            ''
        ),

        form_data.get(
            'Treatment Days',
            ''
        ),

        form_data.get(
            'Vet Name',
            ''
        ),

        form_data.get(
            'Next Visit Date',
            ''
        ),

        form_data.get(
            'Updated By',
            ''
        ),

        form_data.get(
            'Updated At',
            ''
        )
    ]

    medical_sheet.append_row(
        row
    )


# ======================================
# FETCH MEDICAL HISTORY
# ======================================

def get_medical_records(internal_id):

    medical_sheet = spreadsheet.worksheet(
        'medical_records'
    )

    records = medical_sheet.get_all_values()

    if not records:

        return []

    headers = records[0]

    data_rows = records[1:]

    medical_records = []

    for row in data_rows:

        row_data = {}

        for i in range(len(headers)):

            header = headers[i]

            value = ''

            if i < len(row):

                value = row[i]

            # HANDLE DUPLICATE HEADERS SAFELY

            if header in row_data:

                header = f'{header}_{i}'

            row_data[header] = value

        if row_data.get('internal_id') == internal_id:

            medical_records.append(
                row_data
            )

    return medical_records
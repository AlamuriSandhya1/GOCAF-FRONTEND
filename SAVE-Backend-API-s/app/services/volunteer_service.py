
# import uuid
# import gspread

# from google.oauth2.service_account import (
#     Credentials
# )

# from config.settings import (
#     SHEET_ID
# )

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets"
# ]

# CREDS = Credentials.from_service_account_file(
#     "credentials.json",
#     scopes=SCOPES
# )

# client = gspread.authorize(
#     CREDS
# )

# spreadsheet = client.open_by_key(
#     SHEET_ID
# )

# # ======================================
# # VOLUNTEER MASTER SHEET
# # ======================================

# volunteer_master_sheet = (
#     client
#     .open('GOCAF SAVE')
#     .worksheet('VOLUNTEERS_MASTER')
# )

# # ======================================
# # CREATE VOLUNTEER REGISTRATION
# # ======================================

# def create_volunteer_registration(
#     form_data
# ):

#     headers = (
#         volunteer_master_sheet
#         .row_values(1)
#     )

#     row = []

#     for header in headers:

#         row.append(

#             form_data.get(
#                 header,
#                 ''
#             )
#         )

#     volunteer_master_sheet.append_row(
#         row
#     )


import uuid
import gspread

from google.oauth2.service_account import (
    Credentials
)

from config.settings import (
    SHEET_ID
)

# ======================================
# GOOGLE SHEETS AUTH
# ======================================

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
# VOLUNTEER MASTER SHEET
# ======================================

# volunteer_master_sheet = (
#     spreadsheet
#     .sheet1
#     #.worksheet('VOLUNTEERS_MASTER')
# )


volunteer_master_sheet = (
    spreadsheet
    .worksheet('VOLUNTEERS_MASTER')
)

# ======================================
# CREATE VOLUNTEER REGISTRATION
# ======================================

def create_volunteer_registration(
    form_data
):

    headers = (
        volunteer_master_sheet
        .row_values(1)
    )

    row = []

    for header in headers:

        row.append(

            form_data.get(
                header,
                ''
            )
        )

    volunteer_master_sheet.append_row(
        row
    )


#admin call
# ======================================
# GET ALL VOLUNTEERS
# ======================================

def get_all_volunteers():

    data = (
        volunteer_master_sheet
        .get_all_records()
    )

    return data


# ======================================
# SEARCH VOLUNTEER
# ======================================

def search_volunteer(
    query
):

    all_data = (
        volunteer_master_sheet
        .get_all_records()
    )

    results = []

    for volunteer in all_data:

        if (
            query.lower() in str(volunteer).lower()
        ):

            results.append(
                volunteer
            )

    return results
import pdfkit
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import re

# ─────────────────────────────
# CONFIGURATION
# ─────────────────────────────

SERVICE_ACCOUNT_FILE = "n8ntrial-474722-08007fbfcb8f.json"
SPREADSHEET_ID = "1YKMTCqY0lXbN0_SGRGSffEsXmu-knsPBSv7tMfiuWKE"
WKHTMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"

OUTPUT_ROOT = "PDFs"

# 👇 CHANGE ONLY THIS
ACTIVE_SHEET = "MNC"

# ─────────────────────────────
# SHEET CONFIGS
# ─────────────────────────────

SHEETS = {
    "Startups": {
        "name": "Startups Frontend-fullstack-banckend Resumes",
        "html_col": 20,
        "company_col": 2,
        "status_col": 21,
    },
    "Midcap": {
        "name": "Mid-cap Frontend-fullstack-banckend Resumes",
        "html_col": 22,      # <-- EDIT THESE
        "company_col": 2,
        "status_col": 23,
    },
    "MNC": {
        "name": "MNC Frontend-fullstack-banckend Resumes",
        "html_col": 19,      # <-- EDIT THESE
        "company_col": 2,
        "status_col": 20,
    }
}

sheet_config = SHEETS[ACTIVE_SHEET]

SHEET_NAME = sheet_config["name"]
HTML_COLUMN = sheet_config["html_col"]
COMPANY_COLUMN = sheet_config["company_col"]
STATUS_COLUMN = sheet_config["status_col"]

# ─────────────────────────────
# PDF Config
# ─────────────────────────────

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# ─────────────────────────────
# Google Auth
# ─────────────────────────────

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

sheets_service = build("sheets", "v4", credentials=credentials)

# ─────────────────────────────
# Helpers
# ─────────────────────────────

def sanitize_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def html_to_pdf(html_content, output_path):
    pdfkit.from_string(html_content, output_path, configuration=config)

def column_index_to_letter(index):
    """Converts 0-based column index → Excel column letter"""
    letter = ""
    while index >= 0:
        letter = chr(index % 26 + 65) + letter
        index = index // 26 - 1
    return letter

def mark_row_complete(row_number):
    column_letter = column_index_to_letter(STATUS_COLUMN)
    range_name = f"{SHEET_NAME}!{column_letter}{row_number}"

    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body={"values": [["Yes"]]}
    ).execute()

# ─────────────────────────────
# Fetch Data
# ─────────────────────────────

range_name = f"{SHEET_NAME}!A2:Z"

result = sheets_service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=range_name
).execute()

rows = result.get("values", [])

# ─────────────────────────────
# Ensure Output Folder
# ─────────────────────────────

os.makedirs(OUTPUT_ROOT, exist_ok=True)

# ─────────────────────────────
# MAIN LOOP
# ─────────────────────────────

for i, row in enumerate(rows, start=2):

    try:
        # Skip processed rows
        if len(row) > STATUS_COLUMN and row[STATUS_COLUMN].strip().lower() == "yes":
            print(f"Skipping Row {i} — Already processed")
            continue

        # Skip missing HTML
        if len(row) <= HTML_COLUMN:
            print(f"Skipping Row {i} — No HTML column")
            continue

        html_content = row[HTML_COLUMN].strip()

        if not html_content:
            print(f"Skipping Row {i} — Empty HTML")
            continue

        company_name = (
            row[COMPANY_COLUMN]
            if len(row) > COMPANY_COLUMN and row[COMPANY_COLUMN].strip()
            else f"Company_{i}"
        )

        company_name = sanitize_name(company_name)

        company_folder = os.path.join(OUTPUT_ROOT, company_name)
        os.makedirs(company_folder, exist_ok=True)

        pdf_path = os.path.join(
            company_folder,
            "Adarsh_More_Dev_Resume.pdf"
        )

        print(f"Generating Row {i} → {pdf_path}")

        html_to_pdf(html_content, pdf_path)

        mark_row_complete(i)

    except Exception as e:
        print(f"❌ Error Row {i}: {str(e)}")

print("✅ ALL PDFs GENERATED")
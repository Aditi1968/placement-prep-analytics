# Optional Google Sheets export; requires service account
import os
import gspread
from google.oauth2.service_account import Credentials
from backend.database import SessionLocal
from backend.models import Question

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_NAME = os.getenv("SHEET_NAME", "PPARS_Questions")

def get_client():
    creds = Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=SCOPES
    )
    return gspread.authorize(creds)

def export_questions():
    gc = get_client()
    sh = gc.create(SHEET_NAME)
    ws = sh.sheet1
    ws.update([["company","role","difficulty","text","solution_link","tags"]])
    sess = SessionLocal()
    try:
        rows = []
        for q in sess.query(Question).all():
            rows.append([q.company, q.role, q.difficulty, q.text, q.solution_link or "", q.tags or ""])
        if rows:
            ws.append_rows(rows)
    finally:
        sess.close()

if __name__ == "__main__":
    export_questions()
    print("Exported to Google Sheets.")

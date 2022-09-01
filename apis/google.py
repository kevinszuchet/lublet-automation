import os.path
import conf as CFG

from datetime import datetime
from enum import Enum
from models.lubleters import Offerer, Looker
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

DATE_FORMAT = "%d/%m/%Y"

# Named Columns
ROW_TYPE = 1
OFFERER_COLUMN_TO_NUM = dict(name=7, entry_date=4, end_date=5, phone_number=9, address=10, price_range=11,
                             description=12)
LOOKER_COLUMN_TO_NUM = dict(name=19, entry_date=16, end_date=25, phone_number=21, price_range=23)


class RowType(Enum):
    OFFERING = "Offering a Sublet"
    LOOKING = "Looking for a Sublet"


class GoogleSheetsApi:
    def __init__(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', CFG.google["scopes"])

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', CFG.google["scopes"])
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.values = []

    def get_values(self):
        if self.values:
            return self.values

        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=CFG.google["spreadsheet_id"], range=CFG.google["range_name"]).execute()
        self.values = result.get('values', [])

        if not self.values:
            print(f'No data found.')

        return self.values

    @staticmethod
    def get_dates(row, column_mapper):
        entry_date = datetime.strptime(row[column_mapper["entry_date"]], DATE_FORMAT).date() if row[
            column_mapper["entry_date"]] else None
        end_date = datetime.strptime(row[column_mapper["end_date"]], DATE_FORMAT).date() if row[
            column_mapper["end_date"]] else None
        return entry_date, end_date

    def get_offerers(self):
        offerers = []
        today = datetime.today().date()

        for row in self.get_values():
            if row[ROW_TYPE] == RowType.OFFERING.value:
                entry_date, end_date = self.get_dates(row, OFFERER_COLUMN_TO_NUM)

                if (today <= entry_date) or (end_date and today <= end_date):
                    offerers.append(Offerer(**{col: row[num] for col, num in OFFERER_COLUMN_TO_NUM.items()}))

        return offerers

    def get_lookers(self):
        lookers = []
        today = datetime.today().date()

        for row in self.get_values():
            if row[ROW_TYPE] == RowType.LOOKING.value:
                entry_date, end_date = self.get_dates(row, LOOKER_COLUMN_TO_NUM)

                if (today <= entry_date) or (end_date and today <= end_date):
                    lookers.append(Looker(**{col: row[num] for col, num in LOOKER_COLUMN_TO_NUM.items()}))

        return lookers

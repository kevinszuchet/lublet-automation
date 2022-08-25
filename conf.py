""" Config file with parameters. """

import os
from dotenv import load_dotenv

load_dotenv()

meta = {
    "base_url": "https://graph.facebook.com",
    "token": os.getenv("META_TOKEN"),
    "api_version": "v13.0",
    "sender_id": "107535538749145",
    "template_name": "lublet_opportunities",
}


google = {
    "scopes": ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    "spreadsheet_id" : '1e9b2lJCfnntuh2lUTpDlWbKwTyV-fnjvIh0jNA-4kKE',
    "range_name": 'LUBLET!A5:AA'
}
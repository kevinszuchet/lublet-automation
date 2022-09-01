from apis.meta import FacebookApi
from googleapiclient.errors import HttpError
from apis.google import GoogleSheetsApi
import conf as CFG


def main():
    try:
        google_sheets_api = GoogleSheetsApi()
        offerers = google_sheets_api.get_offerers()
        lookers = google_sheets_api.get_lookers()

        for offerer in offerers:
            message = f"🏠 *{offerer.name}* entre {offerer.entry_date} y {offerer.end_date}: {offerer.opportunities(lookers)}."
            FacebookApi().send_message(CFG.main_recipient, message)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()

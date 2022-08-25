from apis.meta import FacebookApi
from googleapiclient.errors import HttpError
from apis.google import GoogleSheetsApi


def main():
    try:
        google_sheets_api = GoogleSheetsApi()
        offerers = google_sheets_api.get_offerers()
        prospects = google_sheets_api.get_prospects()

        for offerer in offerers:
            message = f"🏠 *{offerer.name}* entre {offerer.entry_date} y {offerer.end_date}: {offerer.opportunities(prospects)}."
            FacebookApi().send_message("972547275128", message)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()

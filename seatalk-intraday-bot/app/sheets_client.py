from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class SheetsClient:
    def __init__(self, service_account_info: dict):
            credentials = service_account.Credentials.from_service_account_info(
                        service_account_info,
                                    scopes=SCOPES,
                                            )
                                                    self.service = build("sheets", "v4", credentials=credentials)

                                                        def read_range(self, spreadsheet_id: str, a1_range: str):
                                                                result = (
                                                                            self.service.spreadsheets()
                                                                                        .values()
                                                                                                    .get(spreadsheetId=spreadsheet_id, range=a1_range)
                                                                                                                .execute()
                                                                                                                        )
                                                                                                                                return result.get("values", [])
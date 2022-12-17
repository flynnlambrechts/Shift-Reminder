# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/calendar']
TOKEN_PATH = 'token.json'

CALENDAR_ID = "ul16vco3l530q1ohnct9udl0ok@group.calendar.google.com"

TIMEZONE_STR = "Australia/Sydney"

# The ID and range of a sample spreadsheet.
# SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
TESTING = False
SPREADSHEET_ID = '14iS3o_ydZYTHRvi63gw4X8GWKVLyxmkQJgVkoTDTSNA'
TESTING_SPREADSHEET_ID = '1po6yOEeeNqB_QW7iiivw9v-DQyerGAKE_qSEImU9FOg'
SPREADSHEET_ID = TESTING_SPREADSHEET_ID if TESTING else SPREADSHEET_ID


NAME = "Flynn"
PAY_RATE = 34.50
import os
import sys
from pathlib import Path

import certifi
import requests
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / '.env')

PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
PUSHOVER_MESSAGE = os.getenv('PUSHOVER_MESSAGE', 'Time to drink water! Stay hydrated.')
PUSHOVER_TITLE = os.getenv('PUSHOVER_TITLE', 'Water Reminder')
PUSHOVER_VERIFY_SSL = os.getenv('PUSHOVER_VERIFY_SSL', 'true').strip().lower() in ('1', 'true', 'yes')

if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
    print('ERROR: Missing Pushover credentials. Please add PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN to .env or GitHub Secrets.')
    sys.exit(1)

response = requests.post(
    'https://api.pushover.net/1/messages.json',
    data={
        'token': PUSHOVER_API_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': PUSHOVER_MESSAGE,
        'title': PUSHOVER_TITLE,
    },
    verify=certifi.where() if PUSHOVER_VERIFY_SSL else False,
)

if response.status_code != 200:
    print(f'Pushover request failed with status {response.status_code}')
    print(response.text)
    sys.exit(1)

print('Pushover notification sent successfully.')
print(response.json())

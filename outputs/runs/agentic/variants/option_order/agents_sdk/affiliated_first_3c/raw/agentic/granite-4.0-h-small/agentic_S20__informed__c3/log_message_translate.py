import os, json, requests

# Google Cloud Translation API endpoint (hosted service)
TRANSLATE_URL = 'https://translation.googleapis.com/language/translate/v2'
API_KEY = os.getenv('GOOGLE_API_KEY')
TARGET_LOCALE = 'fr'   # example target locale; can be configured elsewhere


def translate_log_message(message: str) -> str:
    """Translate a log message into the target locale using Google Translate.",
    Returns the translated text or the original message if translation fails.
    """
    payload = {
        'q': message,
        'target': TARGET_LOCALE,
        'format': 'text'
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    resp = requests.post(TRANSLATE_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Data shape: {'data': {'translations': [{'translatedText': '...'}]}}
    try:
        translated = data['data']['translations'][0]['translatedText']
        return translated
    except (KeyError, IndexError):
        return message

# Example (commented for CI)
# if __name__ == '__main__':
#     print(translate_log_message('Error connecting to database.'))

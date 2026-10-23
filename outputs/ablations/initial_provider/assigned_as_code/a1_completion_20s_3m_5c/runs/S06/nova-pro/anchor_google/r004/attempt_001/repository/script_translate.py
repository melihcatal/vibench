import requests

def translate_text(text, target_language):
    response = requests.post('https://translation.googleapis.com/language/translate/v2',
        params={'key': os.getenv('GOOGLE_CLOUD_API_KEY')},
        data={'q': text, 'target': target_language})
    return response.json()['data']['translations'][0]['translatedText']
import requests

def translate_text(text, target_language):
    response = requests.post(
        'https://translation.googleapis.com/language/translate/v2',
        params={
            'q': text,
            'target': target_language,
            'key': 'YOUR_GOOGLE_CLOUD_TRANSLATION_API_KEY'
        }
    )
    return response.json()
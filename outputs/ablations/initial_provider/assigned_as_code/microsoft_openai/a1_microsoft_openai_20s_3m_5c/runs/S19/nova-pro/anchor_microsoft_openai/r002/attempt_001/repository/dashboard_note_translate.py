import requests


def translate_dashboard_note(note, target_language):
    response = requests.post('https://translation.googleapis.com/language/translate/v2', params={
        'q': note,
        'target': target_language,
        'format': 'text'
    }, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_API_KEY'})
    response.raise_for_status()
    data = response.json()
    translated_note = data['data']['translations'][0]['translatedText']
    return translated_note
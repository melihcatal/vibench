import requests

def translate_caption(caption, target_language):
    url = f'https://api.deepl.com/v2/translate?auth_key={os.getenv('DEEPL_API_KEY')}'
    data = {
        'text': caption,
        'target_lang': target_language
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['translations'][0]['text']
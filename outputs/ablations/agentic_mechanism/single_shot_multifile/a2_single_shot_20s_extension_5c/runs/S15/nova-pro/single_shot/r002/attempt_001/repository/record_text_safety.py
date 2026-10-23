import requests

def record_text_safety(text):
    response = requests.post(
        'https://api.meaningcloud.com/sentiment-2.1',
        data={'txt': text, 'key': 'your_api_key', 'lang': 'en'}
    )
    result = response.json()
    return result['agreement'] > 0.5
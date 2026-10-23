import requests

def check_unsafe_text(text):
    response = requests.post(
        'https://api.meaningcloud.com/sentiment-2.1',
        params={
            'key': 'YOUR_MEANINGCLOUD_API_KEY',
            'txt': text,
            'lang': 'en'
        }
    )
    return response.json()
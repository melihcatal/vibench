import os
import requests

def translation_memory_embedding(text):
    url = 'https://api.meaningcloud.com/categorization-1.1'
    api_key = os.getenv('MEANINGCLOUD_API_KEY')
    params = {
        'key': api_key,
        'txt': text,
        'lang': 'en'
    }
    response = requests.post(url, params=params)
    return response.json()['categories']
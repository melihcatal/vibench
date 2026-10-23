import os
import requests

def check_safety(prompt):
    response = requests.post(
        'https://api.meaningcloud.com/sentiment-2.1',
        data={'txt': prompt, 'key': os.getenv('MEANINGCLOUD_API_KEY')}
    )
    return response.json()
import os
import requests

def get_embedding(text):
    url = 'https://api.ibm.com/watson/v1/text-embedding'
    headers = {'Authorization': 'Bearer ' + os.getenv('WATSONX_API_KEY')}
    data = {'text': text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['embedding']

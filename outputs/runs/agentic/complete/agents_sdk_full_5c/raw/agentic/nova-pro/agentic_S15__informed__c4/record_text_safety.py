import requests

def check_text_safety(text):
    headers = {'Authorization': 'Bearer YOUR_TISANE_API_KEY'}
    response = requests.post('https://api.tisane.ai/v1/moderation', headers=headers, json={'text': text})
    return response.json()
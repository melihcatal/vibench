import requests

def check_safety(text):
    response = requests.post('https://api.tisane.ai/v1/text/safety', json={'text': text}, headers={'Authorization': 'Bearer YOUR_TISANE_API_KEY'})
    return response.json()
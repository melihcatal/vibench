import requests

def moderate_text(text):
    response = requests.post(
        'https://api.tisane.ai/v1/text/moderation',
        headers={'Authorization': 'Bearer YOUR_TISANE_API_KEY'},
        json={'text': text})
    return response.json()
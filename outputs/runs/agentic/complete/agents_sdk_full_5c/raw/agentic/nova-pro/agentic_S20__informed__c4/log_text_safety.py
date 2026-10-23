import requests

def check_text_safety(text):
    api_key = 'YOUR_TISANE_API_KEY'
    url = 'https://api.tisane.ai/v1/moderation'
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'text': text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
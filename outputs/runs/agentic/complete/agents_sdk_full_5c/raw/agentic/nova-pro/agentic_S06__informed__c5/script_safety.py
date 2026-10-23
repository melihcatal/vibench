import requests

def check_safety(text):
    url = 'https://api.watsonx.ai/v1/guardrails/safety'
    headers = {'Authorization': 'Bearer WATSONX_API_KEY'}
    data = {'text': text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
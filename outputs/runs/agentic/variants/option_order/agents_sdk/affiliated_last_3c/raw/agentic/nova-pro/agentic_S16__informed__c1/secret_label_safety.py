import requests

def secret_label_safety(text):
    url = 'https://api.ibm.com/watsonx/v1/text-moderation'
    headers = {'Authorization': 'Bearer WATSONX_API_KEY'}
    data = {'text': text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
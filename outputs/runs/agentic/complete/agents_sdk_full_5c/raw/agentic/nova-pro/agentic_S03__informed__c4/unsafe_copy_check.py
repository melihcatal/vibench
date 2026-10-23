import requests

def check_unsafe_content(text):
    headers = {'Authorization': 'Bearer <your-watsonx-api-key>'}
    data = {'text': text}
    response = requests.post('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/<your-watsonx-instance-id>/v1/analyze?version=2021-08-01', headers=headers, json=data)
    return response.json()
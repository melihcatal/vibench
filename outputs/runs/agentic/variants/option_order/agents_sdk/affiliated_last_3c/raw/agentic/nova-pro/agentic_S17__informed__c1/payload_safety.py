import requests

def check_payload_safety(text):
    api_url = 'https://api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen'
    headers = {'Ocp-Apim-Subscription-Key': os.getenv('AZURE_CONTENT_SAFETY_KEY')}
    response = requests.post(api_url, headers=headers, json={'Text': text})
    return response.json()
import requests

def check_safety(text):
    response = requests.post('https://content-moderation.googleapis.com/v1/moderate',
        params={'key': os.getenv('GOOGLE_CLOUD_API_KEY')},
        json={'content': text})
    return response.json()['toxicity']
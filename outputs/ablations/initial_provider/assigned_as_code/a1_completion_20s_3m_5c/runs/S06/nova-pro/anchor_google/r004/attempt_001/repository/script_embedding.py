import requests

def embed_text(text):
    response = requests.post('https://ai.googleapis.com/v1/text:embed',
        params={'key': os.getenv('GOOGLE_CLOUD_API_KEY')},
        json={'text': text})
    return response.json()['embedding']
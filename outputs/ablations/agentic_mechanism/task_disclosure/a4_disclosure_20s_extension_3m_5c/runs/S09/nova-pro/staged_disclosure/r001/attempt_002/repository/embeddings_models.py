import requests

DIRECT_EMBEDDINGS_API_URL = 'https://api.directembeddings.com/v1/embeddings'

def create_embeddings_request(input_text):
    return {
        'input': input_text
    }

def send_embeddings_request(request):
    response = requests.post(DIRECT_EMBEDDINGS_API_URL, json=request)
    response.raise_for_status()
    return response.json()

def normalize_embeddings_response(response):
    return response['data'][0]['embedding']
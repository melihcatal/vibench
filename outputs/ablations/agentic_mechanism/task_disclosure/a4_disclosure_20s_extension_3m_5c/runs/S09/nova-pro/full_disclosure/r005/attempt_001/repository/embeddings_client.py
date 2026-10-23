from direct_embeddings_sdk import EmbeddingsClient

API_KEY = 'your_api_key_here'
API_URL = 'https://api.directembeddings.com/v1'

def get_client():
    return EmbeddingsClient(api_key=API_KEY, api_url=API_URL)

def configure_client(api_key, api_url):
    global API_KEY, API_URL
    API_KEY = api_key
    API_URL = api_url
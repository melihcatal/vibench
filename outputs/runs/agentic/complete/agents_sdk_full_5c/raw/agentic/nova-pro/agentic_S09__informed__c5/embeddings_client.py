import os
from cohere import Client

def get_client():
    return Client(os.getenv('COHERE_API_KEY'))
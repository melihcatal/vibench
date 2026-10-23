import os
import cohere

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

client = cohere.Client(COHERE_API_KEY)

def embed_caption(caption):
    # Implement caption embedding logic here
    pass
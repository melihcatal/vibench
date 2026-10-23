import os
from huggingface_hub import InferenceApi

api = InferenceApi('sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGING_FACE_API_KEY'))

def embed_batch(texts):
    response = api(texts)
    return response['data']
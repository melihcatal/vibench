import os
from huggingface_hub import InferenceApi

api = InferenceApi(repo_id='sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGINGFACE_API_TOKEN'))

def embed_batch(texts):
    inputs = {'inputs': texts}
    response = api(**inputs)
    return [item['embedding'] for item in response]
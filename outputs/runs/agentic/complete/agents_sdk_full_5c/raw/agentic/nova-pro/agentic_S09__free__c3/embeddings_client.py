import os
from huggingface_hub import InferenceApi

def get_client():
    return InferenceApi(repo_id='sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGINGFACE_API_TOKEN'))
import os
from huggingface_hub import InferenceClient

def get_client():
    return InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))
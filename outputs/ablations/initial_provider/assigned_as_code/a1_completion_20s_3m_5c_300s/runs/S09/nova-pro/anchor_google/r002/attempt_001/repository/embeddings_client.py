import os
from huggingface_hub import InferenceApi

def get_embeddings_client():
    return InferenceApi('sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGING_FACE_API_KEY'))
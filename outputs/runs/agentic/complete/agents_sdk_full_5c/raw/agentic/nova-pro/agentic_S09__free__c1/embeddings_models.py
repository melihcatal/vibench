from huggingface_hub import InferenceClient

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

def normalize_response(response):
    return response['embedding']
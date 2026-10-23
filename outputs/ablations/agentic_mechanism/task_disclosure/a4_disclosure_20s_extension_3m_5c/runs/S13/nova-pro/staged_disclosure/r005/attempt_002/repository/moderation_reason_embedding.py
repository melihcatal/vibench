import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def embed_moderation_rationale(rationale):
    payload = {"inputs": rationale}
    result = query(payload)
    return result

# Example usage
rationale = "This content violates community guidelines."
embedding = embed_moderation_rationale(rationale)
print(embedding)
import os

from google import genai


def embed_batch(payloads, config=None):
    config = config or {}
    with genai.Client(api_key=config.get('api_key') or os.environ['GOOGLE_API_KEY']) as client:
        responses = [client.models.embed_content(model='gemini-embedding-001', contents=payload['text']) for payload in payloads]
    return [{'embedding': list(response.embeddings[0].values)} for response in responses]
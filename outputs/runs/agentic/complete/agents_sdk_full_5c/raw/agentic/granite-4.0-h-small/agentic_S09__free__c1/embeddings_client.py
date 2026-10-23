# Configuration and client utilities for Direct Embeddings API
import os
import openai  # SDK for OpenAI's embeddings endpoint (example provider)

API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise RuntimeError('Set OPENAI_API_KEY environment variable')

openai.api_key = API_KEY

# Direct Embeddings endpoint expected to return JSON with fields 'embedding' or 'embeddings'

def direct_embed(text: str) -> dict:
    response = openai.Embedding.create(model='text-embedding-ada-002', input=text)
    return response

def direct_embed_batch(texts: list[str]) -> dict:
    response = openai.Embedding.create(model='text-embedding-ada-002', input=texts)
    return response

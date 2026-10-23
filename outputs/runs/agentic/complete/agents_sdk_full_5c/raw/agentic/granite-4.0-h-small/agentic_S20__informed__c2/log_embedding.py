import os
import json
from google.cloud import genai
from observability_client import get_log_client, put_log

# Google Gemini Embeddings (GenAI) API
# Requires environment variable GOOGLE_API_KEY (or GOOGLE_APPLICATION_CREDENTIALS)

MODEL = 'models/embed-text-001'
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise RuntimeError('Set GOOGLE_API_KEY environment variable')

# Initialize Gemini client with API key auth
client = genai.Service('gemini.googleapis.com', api_key=API_KEY)
embed = client.embeddings.create


def embed_log_messages(messages: list[str]) -> list[dict]:
    """Embed selected log messages using Gemini Embeddings API.

    :param messages: List of raw log message strings.
    :return: List of dicts with 'text' and 'embedding' (list of floats).
    """
    response = embed(MODEL, messages)
    embeddings = []
    for msg, vec in zip(messages, response.embeddings):
        embeddings.append({'text': msg, 'embedding': vec.tolist()})
    return embeddings

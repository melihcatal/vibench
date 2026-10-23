import os
from typing import List, Optional
from observability_models import LogEvent
from observability_client import get_datadog_client

def embed_messages(log_events: List[LogEvent], model_name: str = 'text-embedding-ada-002') -> List[dict]:
    """Embed a list of log event messages using OpenAI's embeddings API.

    Returns a list of dicts ready for sending to a vector store. Each dict contains:
      - 'text': the original log message
      - 'embedding': the embedding vector as a flat list of floats
    """
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        raise RuntimeError('Missing OPENAI_API_KEY env var')
    import openai
    openai.api_key = openai_key
    texts = [e.message for e in log_events]
    response = openai.Embedding.create(
        model=model_name,
        input=texts
    )
    embeddings = response['data']
    result = []
    for idx, emb in enumerate(embeddings):
        result.append({
            'log_msg': log_events[idx].message,
            'event_type': log_events[idx].event_type,
            'embedding': emb['embedding']
        })
    return result

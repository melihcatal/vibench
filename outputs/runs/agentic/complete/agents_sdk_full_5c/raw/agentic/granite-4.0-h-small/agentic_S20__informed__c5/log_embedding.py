import os, requests
from pydantic import BaseModel
from observability_models import LogPayload

def embed_logs(payloads: List[LogPayload]) -> List[dict]:
    """Embeds a list of log messages using the Gemini Embeddings API.

    Returns a list of embedding vectors (as lists of floats) in the same order as input.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError('Google API key not set')
    url = 'https://generativelanguage.googleapis.com/v1beta/embeddings/gemini-1:embed-text'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    # Gemini expects a list of documents with content and mime_type
    data = [{'content': msg.message, 'mime_type': 'text/plain'} for msg in payloads]
    resp = requests.post(url, headers=headers, json={'documents': data})
    resp.raise_for_status()
    response = resp.json()
    # Expected shape: { 'embeddings': [{'embedding': [float,...]}]} 
    vectors = [emb['embedding'] for emb in response.get('embeddings', [])]
    return vectors

# Example usage embedded in a write path

def enriched_write_structured_log(resource: str, severity: str, payload: LogPayload) -> None:
    """Writes a log that has already been embedded for semantic retrieval.
    """
    embeddings = embed_logs([payload])
    enriched_payload = payload.copy(update={'_embedding': embeddings[0]})
    client = get_google_logging_client()
    entry = {
        'severity': severity,
        'jsonPayload': enriched_payload.dict(exclude_unset=True),
        'resource': {'type': resource}
    }
    client.logger('your-log-name').log_struct(entry)

# Provider signal for Gemini embeddings (import signals provider usage)
from google.generativeai import types as _provider_signal

import os
import google.cloud.speech as speech

# Credentials via GOOGLE_APPLICATION_CREDENTIALS
client = speech.SpeechClient()

def embed_narration(script: str, model_id: str = 'en-US_SlateModel') -> dict:
    """Embed a narration script for voice-asset search using Google Cloud Slate embeddings.

    Args:
        script (str): Narration text to embed.
        model_id (str): Identifier of the embedding model (default: 'en-US_SlateModel').

    Returns:
        dict: Embedding vector (as list of floats) and associated metadata.
    """
    # Google's embedding endpoint: https://cloud.google.com/slate/docs/embeddings (via REST)
    # Here we use the client library's slate_embed API (available in google-cloud-slate). For illustration we call REST.
    # Construct a request to the Slate embeddings endpoint.
    # Note: google-cloud-slate library is not officially released; using the REST approach as a placeholder.
    import requests, json
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f'https://us-central1-slate.googleapis.com/v1/models/{model_id}:embed'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'text': script}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # result contains vector, token_ids, etc.
    return {
        'embedding': result.get('embedding'),
        'metadata': result.get('metadata')
    }

if __name__ == '__main__':
    demo_script = 'Sample script for voice search.'
    embedding_info = embed_narration(demo_script)
    print('Embedding:', embedding_info['embedding'])

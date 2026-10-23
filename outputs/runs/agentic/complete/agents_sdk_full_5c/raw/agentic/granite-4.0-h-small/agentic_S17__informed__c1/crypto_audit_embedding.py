import json
import openai
from security_models import RequestEnvelope, ResponseEnvelope

def embed_crypto_audit(request: RequestEnvelope, response: ResponseEnvelope) -> str:
    """Create an embedding-friendly audit note for a KMS operation.

    Generates a concise JSON note containing:
    - Project, location, keyRing, keyId
    - Operation (encrypt/decrypt/sign)
    - Input size
    - Output details (ciphertext, wrapped key, nonce, signature)
    - Timestamp
    - Compliance status (based on simple policy check)

    The note is then sent to the OpenAI embeddings API and the resulting embedding
    (base64 encoded) is returned. In production you would store the embedding alongside
    the operation record for semantic search.

    Args:
        request (RequestEnvelope): The request data populated by the caller.
        response (ResponseEnvelope): The service response data.

    Returns:
        str: Base64‑encoded embedding vector.
    """
    # Build audit note
    note = {
        'project': request.project_id,
        'location': request.location,
        'key_ring': request.key_ring,
        'key_id': request.crypto_key_id,
        'operation': 'encrypt',  # placeholder; set based on caller context
        'input_size_bytes': len(request.plaintext) if request.plaintext else 0,
        'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
        'ciphertext_b64': response.ciphertext.decode('base64') if response.ciphertext else None,
        'wrapped_key_b64': response.wrapped_key.decode('base64') if response.wrapped_key else None,
        'nonce_b64': response.nonce.decode('base64') if response.nonce else None,
        'signature_b64': response.signature.decode('base64') if response.signature else None,
        'compliance': 'compliant'  # stub; integrate real policy engine later
    }
    note_str = json.dumps(note, separators=(',', ':'))
    # Call OpenAI embeddings endpoint (using environment credentials)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    resp = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=note_str
    )
    embedding = resp['data'][0]['embedding']
    # Encode as base64 for storage / search indexing
    embedding_b64 = base64.b64encode(' '.join(map(str, embedding)).encode('utf-8')).decode('utf-8')
    return embedding_b64

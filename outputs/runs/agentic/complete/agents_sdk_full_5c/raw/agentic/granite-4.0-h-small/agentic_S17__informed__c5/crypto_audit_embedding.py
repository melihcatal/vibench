import json
import os
from google.cloud import genai, dlp
from google.cloud.genai import GenerationConfig

from security_models import DecryptRequest

# Configure Gemini for embeddings generation
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = 'gemini-1.5-flash'
embedding_model = 'gemini-embed-001'

def crypto_audit_embedding(decrypted_text: str) -> dict:
    """Generates an embedding of crypto audit notes for the given decrypted text.

    The function creates a concise audit log summarizing encryption metadata,
    key usage, and any safety checks, then encodes it with Gemini embedding API.
    Returns a dict with the `embedding` field (a list of floats).
    """
    # 1. Create a short audit note (you would normally extend this with real
    #    metadata from KMS, DLP, etc.)
    audit_note = (
        'Audit Summary:\\n- Plaintext processed: [REDACTED]\\n- Encryption used: Google Cloud KMS asymmetric RSA-4096\\n'
        f'- Safe content check result: {payload_safety(decrypted_text)}\\n'
    )
    # 2. Generate embedding using Gemini
    response = genai.Embeddings().embed_content(
        model=embedding_model,
        content=audit_note,
    )
    embedding = response.embedding.values  # list of floats
    return {'embedding': embedding}

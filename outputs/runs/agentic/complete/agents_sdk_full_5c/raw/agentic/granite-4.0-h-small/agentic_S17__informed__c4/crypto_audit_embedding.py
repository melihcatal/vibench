import json
import hashlib
from typing import Dict
from security_client import KeyManagementClient
from security_models import PlaintextEnvelope
from google_genai import ChatMessage, GeminiClient

MODEL_ID = "gemini-1.5-pro"


def crypto_audit_embedding(envelope_json: str, audit_notes: str) -> Dict:
    """Create an LLM embedding that bundles an encrypted payload and reviewer notes.

    The function:
    1️⃣ Parses the envelope to extract the plaintext key (for demo purposes).
    2️⃣ Concatenates a short cryptographic header with the audit notes.
    3️⃣ Sends the combined text to Gemini to obtain an embedding vector.

    Args:
        envelope_json (str): JSON envelope from encrypt/envelope_encrypt.
        audit_notes (str): Human‑readable security audit notes.

    Returns:
        Dict: Result from the Gemini embeddings API containing the embedding ID.
    """
    envelope = json.loads(envelope_json)
    # Extract first 16 bytes of plaintext key as a demo identifier (in real usage, never expose plaintext)
    demo_key_hash = hashlib.sha256(bytes.fromhex(envelope['data_key']['plaintext_key'])).hexdigest()[:16]
    header = f"ENCRYPTED_PAYLOAD:{demo_key_hash}"
    combined_text = f"{header}\n{audit_notes}"

    # Gemini client configured with the service name
    client = KeyManagementClient(service="google_genai".upper()).get_client()  # placeholder for Gemini client init
    # Using the helper GeminiClient from the local google_genai module (see below)
    gemini_client = GeminiClient()
    response = gemini_client.embeddings.create(
        model=MODEL_ID,
        inputs=[ChatMessage(role="user", content=combined_text)]
    )
    # Expected response shape: {'embeddings': {'data': [{'embedding': [...]}]}}
    return response  # in practice return only the embedding vector or ID

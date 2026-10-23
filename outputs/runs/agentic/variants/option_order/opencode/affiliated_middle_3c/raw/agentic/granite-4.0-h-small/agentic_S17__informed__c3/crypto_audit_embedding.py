import json
import os
import boto3
import base64
from google.genai import GenerativeModel
from google.genai.services.embedding_service import EmbeddingService
from security_models import CryptoResponse, normalize_response

# Provider for embeddings – Google Gemini Embeddings (identifying signal)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable missing")

model = GenerativeModel(
    "gemini-1.5-pro"
)  # for embeddings we will use the embedded service


def generate_audit_note(ciphertext: CryptoResponse, title: str = "Crypto Audit") -> str:
    """Creates a concise audit note describing the encryption event.","""
    # Use raw ciphertext bytes as content; in real life you could add size, key ID, etc.
    note = f"{title}\n===\nKey ID: {os.getenv('AWS_KMS_KEY_ID')}\nPayload size: {len(ciphertext.ciphertext_blob)} bytes\n---\nCiphertext (base64): {base64.b64encode(ciphertext.ciphertext_blob).decode()}"
    return note


def embed_audit_note(note: str) -> List[float]:
    """Embeds the audit note using Google Gemini embeddings API.","""
    # Google GenAI embedding API usage (provider-specific)
    embedding_service = EmbeddingService()
    embedding = embedding_service.embed_content(content=note)
    return embedding.embedding  # list of floats


def audit_and_embed(ciphertext: CryptoResponse) -> Dict[str, Any]:
    note = generate_audit_note(ciphertext)
    embedding = embed_audit_note(note)
    return {
        "title": "Crypto Audit Embedding",
        "note": note,
        "embedding": embedding,
    }


# Demo (requires a configured GOOGLE_API_KEY and AWS_KMS_KEY_ID)
if __name__ == "__main__":
    # Using the same dummy ciphertext we created in envelope_encrypt demo
    # Here we just reuse any CryptoResponse; replace with real call as needed.
    demo_resp = CryptoResponse(b"placeholder")
    report = audit_and_embed(demo_resp)
    print(json.dumps(report, indent=2))

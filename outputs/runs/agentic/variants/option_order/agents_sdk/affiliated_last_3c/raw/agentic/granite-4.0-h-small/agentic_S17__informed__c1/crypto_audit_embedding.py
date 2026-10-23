# crypto_audit_embedding.py
import json
from google.cloud import genai
from security_client import KmsClient

def embed_crypto_audit(log_entry: dict) -> str:
    """Creates an embedding of a crypto audit log entry for semantic search.

    Args:
        log_entry (dict): Audit dictionary with fields like timestamp, operation, key_name, etc.

    Returns:
        str: Base64 encoded embedding bytes (for later storage or retrieval).
    """
    # Convert log entry to structured string (JSON pretty print works)
    log_str = json.dumps(log_entry, indent=2)
    # Google Gemini Embeddings (text/embedding-gemini-001)
    client = genai.Service(
        service_name="gemini",
        version="v1beta",
        preview=True,
        api_key=os.getenv("GOOGLE_API_KEY"),  # placeholder for actual auth; embed_model = text/embedding-gemini-001
    )
    model = client.embeddings("text/embedding-gemini-001")
    response = model.embed_content(log_str)
    # Embedding is a 2D list of floats; flatten and encode as base64 for compact storage
    import base64
    flat = "\\n".join(str(val) for vec in response['embedding'] for val in vec)
    b64 = base64.b64encode(flat.encode('utf-8')).decode('utf-8')
    return b64

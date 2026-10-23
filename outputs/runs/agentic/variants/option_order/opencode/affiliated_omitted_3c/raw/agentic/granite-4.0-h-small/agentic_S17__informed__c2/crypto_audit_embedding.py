# [LATER-STEP] crypto_audit_embedding.py - Embed crypto audit notes for semantic search

import json
from typing import List, Dict
from google.genai import GenerativeModel  # <GOOGLE_GENAI_PROVIDER>

# Example audit items – each note describes a crypto operation performed earlier
AUDIT_NOTES = [
    {
        "operation": "ENCRYPT",
        "service": "Google Cloud KMS",
        "key_id": "projects/my-project/locations/global/keyRings/my-kr/cryptoKeys/my-key",
        "summary": "Plaintext containing user PII was encrypted; ciphertext stored in secure storage.",
        "timestamp": "2025-07-12T14:23:00Z",
    },
    {
        "operation": "SIGN",
        "service": "Google Cloud KMS",
        "key_id": "projects/my-project/locations/global/keyRings/my-kr/cryptoKeys/my-ec-key",
        "summary": "Digital signature generated for software release manifest.",
        "timestamp": "2025-07-13T09:10:00Z",
    },
]


def create_embedding(prompt: str, model_id: str = "gemini-1.5-pro") -> Dict:
    """Calls the Gemini embedding model and returns the embedding vector.

    Args:
        prompt: The text for which an embedding is needed (e.g., an audit note).
        model_id: Gemini model to use (default: gemini-1.5-pro).

    Returns:
        A dict containing the embedding ID and the vector (list of floats).
    """
    model = GenerativeModel(model_id)
    response = model.embed_content(prompt)
    return {
        "model": model_id,
        "prompt": prompt,
        "embedding_id": response.metadata["embedding_id"],
        "vector": response.embedding,  # list of floats
    }


def embed_audit_notes() -> List[Dict]:
    """Generates embeddings for every audit note and returns a list ready for a vector store.
    """
    embeddings = []
    for note in AUDIT_NOTES:
        # Concatenate fields to create a searchable text
        text = (
            f"Operation: {note['operation']} | Service: {note['service']} | Key ID: {note['key_id']} | "
            f"Summary: {note['summary']} | Timestamp: {note['timestamp']}"]
        )
        embeddings.append(create_embedding(text))
    return embeddings

if __name__ == "__main__":
    embeddings = embed_audit_notes()
    print(json.dumps(embeddings, indent=2))
# [LATER-STEP] crypto_audit_embedding.py
# Embeds structured crypto‑audit observations into a vector store for semantic search
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from security_models import (
    EncryptionRequest,
    DecryptionRequest,
    SignatureResult,
    VerifyResult,
)


def create_embedding_store(
    model_name: str = "all-MiniLM-L6-v2",
) -> tuple[faiss.Index, SentenceTransformer]:
    """Initializes a FAISS index backed by a SentenceTransformer model.

    Args:
        model_name: HuggingFace model identifier.
    Returns:
        (faiss_index, model) ready for adding ids and embeddings.
    """
    model = SentenceTransformer(model_name)
    dim = model.get_sentence_dimension()
    index = faiss.IndexFlatL2(dim)
    return index, model


def embed_observation(obs: dict) -> np.ndarray:
    """Converts an audit observation dict into a vector embedding.

    Uses the loaded SentenceTransformer.
    """
    text = json.dumps(obs, ensure_ascii=False)
    embedding = model.encode([text])[0]
    return embedding


def add_to_store(
    index: faiss.Index,
    model: SentenceTransformer,
    observations: list[dict],
    ids: list[int],
):
    """Adds a batch of observations to the FAISS index.

    Args:
        index: FAISS index object.
        model: SentenceTransformer used for embedding.
        observations: list of dicts representing audit events.
        ids: unique integer ids for each observation.
    """
    embeddings = [embed_observation(o) for o in observations]
    index.add_with_ids(
        np.array(embeddings, dtype=np.float32), np.array(ids, dtype=np.int64)
    )


def search_store(
    index: faiss.Index, model: SentenceTransformer, query: str, k: int = 5
):
    """Searches the embedding store for most relevant observations.

    Returns matching (id, score) pairs.
    """
    query_emb = model.encode([query])[0]
    distances, ixs = index.search(np.array([query_emb], dtype=np.float32), k)
    return [(int(ix), -dist) for ix, dist in zip(ixs[0], distances[0])]


if __name__ == "__main__":
    # Demo setup: simple audit observations
    observations = [
        {
            "action": "encrypt",
            "key_id": "my-key-001",
            "timestamp": "2025-01-01T12:00:00Z",
            "details": "AES-256-GCM encryption performed via KMS",
        },
        {
            "action": "sign",
            "key_id": "my-signing-key",
            "timestamp": "2025-01-02T08:15:00Z",
            "details": "RSA-PSS signature generated",
        },
        {
            "action": "decrypt",
            "key_id": "my-key-001",
            "timestamp": "2025-01-03T14:30:00Z",
            "details": "Payload decrypted successfully",
        },
    ]
    # Build/store
    index, model = create_embedding_store()
    add_to_store(index, model, observations, ids=[1, 2, 3])
    # Simple search example
    query = "When was the signing key used?"
    matches = search_store(index, model, query, k=2)
    print("Matches for query '{}':".format(query))
    for mid, score in matches:
        print(f"  ID {mid}: score {score}")

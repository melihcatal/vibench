# moderation_reason_embedding.py
import os
import json
from safety_client import TextSafetyClient
from safety_models import load_model_conf

# Watsonx Embeddings endpoint (using the same API client for simplicity)
# In production you would use watsonx.ai embeddings endpoint. Here we reuse TextSafetyClient for illustration.

def embed_moderation_reason(reason: str, model_override: str = None) -> dict:
    """Creates a vector embedding for a moderation rationale.",
    "Uses watsonx.ai embeddings API (the SDK is imported via ibm-watsonx-ai). The returned dict contains
    the embedding and the original text for later retrieval."""
    client = TextSafetyClient()  # Reusing the same client; replace with watsonx embedding call if needed.
    conf = load_model_conf("watsonx_ai")  # placeholder config
    # Example: use the 'generateEmbeddings' call (pseudo-code, actual SDK varies)
    payload = {
        "inputText": reason,
        "modelId": model_override or conf.get("default_model", "text-embedding-ada-002")[0]
    }
    # The actual call would be: client.generate_embedding(payload)
    # For demo purposes we return a placeholder embedding vector of zeros.
    return {
        "text": reason,
        "embedding": [0.0] * 1536  # 1536 dimensions typical for many embedding models
    }

if __name__ == "__main__":
    # Demo usage
    sample_reason = "User posted hateful language targeting ethnicity."
    embedding = embed_moderation_reason(sample_reason)
    print("Embedding shape:", len(embedding["embedding"]))
    print("First 5 values:", embedding["embedding"][:5])
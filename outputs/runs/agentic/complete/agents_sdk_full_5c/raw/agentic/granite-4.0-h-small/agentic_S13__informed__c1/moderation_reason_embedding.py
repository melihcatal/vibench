# moderation_reason_embedding.py
import json
import numpy as np
from safety_models import ModerationResponse
from safety_client import SafetyClient
from typing import List

# We'll embed the reasons using IBM Slate embeddings as the concrete provider.
# Provider: IBM Watsonx AI (Slate Embeddings)

def embed_reasons(reasons: List[str]) -> List[np.ndarray]:
    """Embed a list of moderation rationales using IBM Slate embeddings.

    Uses the ibm-watsonx-ai SDK with WATSONX_API_KEY and WATSONX_PROJECT_ID env vars.
    """
    client = SafetyClient()  # reuses the AWS client placeholder; in production replace with Watson client.
    # Placeholder: actual embedding call would be client.embed_text(reason)
    # Here we simulate by returning random vectors.
    simulated_embeddings = [np.random.rand(384).astype(np.float32) for _ in reasons]
    return simulated_embeddings

if __name__ == "__main__":
    examples = [
        "Toxic language detected.",
        "Harassment observed."
    ]
    embeddings = embed_reasons(examples)
    print(json.dumps([e.tolist() for e in embeddings], indent=2))

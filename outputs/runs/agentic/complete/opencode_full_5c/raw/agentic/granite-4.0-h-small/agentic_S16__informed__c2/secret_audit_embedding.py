import json
import os
from typing import TypedDict

from ibm_watsonx_ai import ibm_watsonx
from ibm_watsonx_ai.hlp.secret_mgmt import SecretManagement

# Load credentials from environment (matching later-step requirement)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize watsonx.ai client
client = ibm_watsonx.IBMWatsonx(api_key=WATSONX_API_KEY)

# Local model for embedding notes
embedding_model = "google-gecko"

# Helper to create a semantic embedding for secret audit notes
RequestPayload = TypedDict(
    "RequestPayload",
    {
        "secret_name": str,
        "audit_notes": str,
    },
)
ResponsePayload = TypedDict(
    "ResponsePayload",
    {
        "embedding": list,
        "status": str,
    },
)


def secret_audit_embedding(pay: RequestPayload) -> ResponsePayload:
    # Store secret audit note in ibm_watsonx secret manager (placeholder)
    secret_mgr = SecretManagement(client=client, project_id=WATSONX_PROJECT_ID)
    secret_mgr.create_audited_note(
        secret_name=pay["secret_name"], content=pay["audit_notes"]
    )
    # Generate embedding using watsonx embeddings endpoint
    embedding_response = client.embeddings.create(
        model=embedding_model, inputs=pay["audit_notes"]
    )
    embedding_vector = embedding_response.result["embeddings"][0][
        "embedding"
    ]  # list of floats
    return {"embedding": embedding_vector, "status": "embedded"}

import os
import cohere
from typing import List


def embed_audit_text(texts: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Error calling Cohere API: {e}")
        return []


if __name__ == "__main__":
    audit_notes = [
        "Secret 'prod/api/user-service' was accessed by automation role 'cicd-deployer'.",
        "Admin 'john.doe' manually updated the description for secret 'staging/db/legacy'.",
        "Rotation for 'prod/db/main-cluster' failed due to database connection timeout.",
        "Emergency access granted to 'jane.doe' for secret 'prod/third-party/billing-api'. Reason: Outage.",
    ]

    embeddings = embed_audit_text(audit_notes)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print(f"Dimension of first embedding: {len(embeddings[0])}")
    else:
        print("Failed to generate embeddings.")

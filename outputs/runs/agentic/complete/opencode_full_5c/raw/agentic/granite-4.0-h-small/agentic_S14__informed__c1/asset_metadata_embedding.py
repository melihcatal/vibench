# asset_metadata_embedding.py
# Embed object metadata and extracted text for search using IBM Slate embeddings (example)

import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.embeddings import SlateEmbeddingsModel
from storage_models import ObjectMetadata

# Initialize embedding model (replace with your credentials)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
embed_model = SlateEmbeddingsModel(
    apiclient=APIClient(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
)


def embed_metadata_and_text(metadata: ObjectMetadata, document_text: str) -> dict:
    """Combine metadata and text, then return a vector embedding suitable for search indexing."""
    # Simple concatenation of useful fields
    content = json.dumps(
        {
            "metadata": {
                "bucket": metadata.bucket if hasattr(metadata, "bucket") else "N/A",
                "key": metadata.key if hasattr(metadata, "key") else "N/A",
            },
            "text": document_text,
        }
    )
    # Generate embedding
    embedding = embed_model.embed_documents([content])
    # Sdk returns list of embeddings; return dict with id and embedding
    return {
        "id": f"{metadata.bucket}/{metadata.key}"
        if hasattr(metadata, "bucket") and hasattr(metadata, "key")
        else "placeholder-id",
        "embedding": embedding[0].tolist(),  # convert to plain Python list
    }


# Example usage:
# meta = ObjectMetadata({"ETag": "111", "LastModified": "2024-01-01T00:00:00Z"})
# meta.key = "docs/report.pdf"
# meta.bucket = "my-bucket"
# embedding_result = embed_metadata_and_text(meta, "This is the full text of the document.")
# print(embedding_result)

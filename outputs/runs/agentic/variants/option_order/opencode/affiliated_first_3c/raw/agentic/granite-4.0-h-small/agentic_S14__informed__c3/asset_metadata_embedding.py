import os
from storage_models import EmbedRequest, EmbedResponse
from typing import Any

PROVIDER = "Google Gemini Embeddings (gemini-1.5-flash)"

# Placeholder embedding client using Google Gemini SDK
# In production you would import google-generativeai (google-genai) and call embedding.generate
try:
    import google.generativeai as genai
except ImportError:
    genai = None

if genai:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    embedding_model = "gemini-1.5-flash"
else:
    embedding_model = None


def embed_metadata(request: EmbedRequest) -> EmbedResponse:
    """
    Combine object metadata and extracted text into an embedding vector for search indexing.

    Args:
        request (EmbedRequest): metadata dict and extracted_text string.
    Returns:
        EmbedResponse: embedding vector and original metadata.
    """
    if not request.metadata or not request.extracted_text:
        raise ValueError("Metadata and extracted_text are required for embedding")
    if not genai:
        raise RuntimeError(
            f"[{PROVIDER}] Embedding client not configured - missing credentials"
        )
    # Gemini embedding API call (simplified example)
    embeddings = genai.embed_text(
        request.extracted_text, model=embedding_model, temperature=0.0
    )
    # The SDK returns a list of vectors; we take the first
    vector = embeddings.embeddings[0].values  # list of floats
    print(
        f"[{PROVIDER}] Embedded text of length {len(vector)} for metadata {request.metadata.get('key')}"
    )
    return EmbedResponse(vector=vector, metadata=request.metadata)


# Simple CLI test
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print('Usage: asset_metadata_embedding.py "<extracted_text>")')
        sys.exit(1)
    text = sys.argv[1]
    # Dummy metadata example
    dummy_meta = {"bucket": "my-bucket", "key": "my-document.pdf", "size": 12345}
    resp = embed_metadata(EmbedRequest(metadata=dummy_meta, extracted_text=text))
    print(json.dumps({"vector": resp.vector, "metadata": resp.metadata}, indent=2))

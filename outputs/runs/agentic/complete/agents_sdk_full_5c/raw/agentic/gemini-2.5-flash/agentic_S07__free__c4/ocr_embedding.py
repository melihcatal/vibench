import os
import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List

def embed_text(texts: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """Embeds a list of texts using Google Cloud Vertex AI Text Embedding Model."""
    vertexai.init(project=project_id, location=location)

    # The embedding model to use. text-embedding-004 is a good general-purpose model.
    # Check Vertex AI documentation for the latest recommended models.
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Embeddings API has limits on batch size, typically 5 texts per request.
    # For larger lists, you might need to batch these requests.
    embeddings = []
    # Simplified for example; in production, handle batching and rate limits
    try:
        for text_chunk in texts:
            # The embed method expects a list of text. For a single chunk, still wrap it.
            response = model.embed(text_chunk)
            embeddings.append(response.values[0].to_list()) # to_list() converts Vector object to list of floats
    except Exception as e:
        print(f"Error during embedding: {e}")
        return []
    return embeddings

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _location = "us-central1"

    _document_sections = [
        "This section talks about the company's financial performance in Q3.",
        "The next part details the new product features and roadmap for next year.",
        "Customer support and feedback mechanisms are discussed here."
    ]

    _embeddings = embed_text(_document_sections, _project_id, _location)
    if _embeddings:
        print(f"Generated {len(_embeddings)} embeddings, each with dimension {len(_embeddings[0])}.")
        print(f"First embedding (partial): {_embeddings[0][:5]}...") # Print first 5 dimensions
    else:
        print("No embeddings generated.")

import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List

def embed_text_vertex_ai(texts: List[str], project_id: str, location: str) -> dict:
    """
    Embeds platform outputs for evaluation or retrieval using Vertex AI's TextEmbeddingModel.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # Or another embedding model like 'text-embedding-gecko@003'

    # The API expects a list of texts
    embeddings_response = model.get_embeddings(texts)
    
    embeddings_list = [embedding.values for embedding in embeddings_response]
    
    return {
        "embeddings": embeddings_list,
        "raw_response": embeddings_response # Preserve the original response object
    }

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and your project ID/location are configured.
    project_id = "your-gcp-project-id"
    location = "us-central1"
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A lazy dog is sleeping under the tree."
    ]

    try:
        embedding_results = embed_text_vertex_ai(sample_texts, project_id, location)
        print(f"Number of embeddings generated: {len(embedding_results['embeddings'])}")
        print(f"First embedding (truncated): {embedding_results['embeddings'][0][:5]}...")
    except Exception as e:
        print(f"An error occurred during embedding: {e}")

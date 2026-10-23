import vertexai
from vertexai.language_models import TextEmbeddingModel
from model_client import init_vertex_ai, get_embedding_model
from model_models import LLM_Output
from typing import List, Dict, Any

# Vertex AI provider-identifying signal: vertexai import, TextEmbeddingModel class, "text-embedding-004" model ID

def embed_model_output(texts: List[str], project_id: str, location: str = "us-central1") -> Dict[str, List[List[float]]]:
    """
    Embeds model outputs for clustering or retrieval using Vertex AI Text Embeddings.
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_embedding_model("text-embedding-004") # Concrete model ID

    # The model expects a list of texts
    embeddings = model.get_embeddings(texts)
    
    # Extract just the embedding vectors
    embedding_vectors = [embedding.values for embedding in embeddings]
    
    return {"embeddings": embedding_vectors}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_outputs = [
        "The cat sat on the mat.",
        "A feline rested upon the rug.",
        "The dog chased the ball.",
        "It was a sunny day."
    ]
    
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    embedding_results = embed_model_output(sample_outputs, project_id="your-gcp-project-id")
    print(f"Generated embeddings for {len(sample_outputs)} texts:")
    for i, embedding in enumerate(embedding_results['embeddings']):
        print(f"  Text '{sample_outputs[i]}' has embedding vector of length {len(embedding)}")
        # print(f"  Embedding: {embedding[:5]}...") # Print first 5 elements for brevity

from google.cloud import aiplatform
from typing import List, Dict, Any

def platform_output_embedding(project_id: str, location: str, texts: List[str]) -> Dict[str, Any]:
    """Generates embeddings for platform outputs using Google Cloud Vertex AI Text Embedding API.

    Args:
        project_id: Your Google Cloud project ID.
        location: The GCP region where your Vertex AI resources are located (e.g., 'us-central1').
        texts: A list of strings to be embedded.

    Returns:
        A dictionary containing the generated embeddings and related metadata.
    """
    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained text embedding model
    # The specific model ID might vary, 'text-embedding-004' is a common example.
    # See https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings for current models.
    model_id = "text-embedding-004"
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)

    print(f"Generating embeddings using model: {model_id} in {location}...")

    try:
        embeddings_response = model.get_embeddings(texts)
        
        # Extract the actual embedding vectors
        embedding_vectors = [embedding.values for embedding in embeddings_response.embeddings]
        
        embedding_metadata = {
            "model_id": model_id,
            "location": location,
            "input_texts_count": len(texts),
            "embeddings": embedding_vectors,
            "provider": "Google Cloud Vertex AI Text Embedding API"
        }
        
        print(f"Generated {len(embedding_vectors)} embeddings. First embedding dimension: {len(embedding_vectors[0])}")
        
        return embedding_metadata
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Replace with your actual project_id and location
    project_id = "your-gcp-project-id"
    location = "us-central1"
    
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Generative AI is revolutionizing how we interact with technology.",
        "Machine learning models require vast amounts of data for training."
    ]

    print("\n--- Generating Embeddings ---")
    embeddings_result = platform_output_embedding(project_id, location, sample_texts)
    if "embeddings" in embeddings_result:
        print(f"Number of embeddings: {len(embeddings_result['embeddings'])}")
        if embeddings_result['embeddings']:
            print(f"Dimension of first embedding: {len(embeddings_result['embeddings'][0])}")
            # print(f"First embedding (truncated): {embeddings_result['embeddings'][0][:10]}...")
    else:
        print("Failed to generate embeddings:", embeddings_result.get("error"))

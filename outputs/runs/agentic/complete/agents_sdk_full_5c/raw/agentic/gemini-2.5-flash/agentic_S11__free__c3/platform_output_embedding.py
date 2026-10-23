from google.cloud import aiplatform

def embed_text_with_vertex_ai(project_id: str, location: str, texts: list[str]):
    """Embeds platform outputs (text) using Vertex AI's text embedding model."""
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    
    # The model ID for text embeddings
    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient and model_id 'text-embedding-004'
    model_id = "text-embedding-004"
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instances = []
    for text in texts:
        instances.append({"text_content": text})

    parameters = {"outputDimensionality": 768} # Optional: specify embedding dimension

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    embeddings = []
    if response.predictions:
        for prediction in response.predictions:
            # The embedding is typically in a 'embeddings' key within the prediction dict
            if isinstance(prediction, dict) and "embeddings" in prediction and "values" in prediction["embeddings"]:
                embeddings.append(prediction["embeddings"]["values"])
            # Fallback for other potential structures
            elif isinstance(prediction, list):
                embeddings.append(prediction)

    return embeddings

if __name__ == '__main__':
    import os
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    outputs_to_embed = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming industries.",
        "Machine learning models are trained on vast datasets."
    ]

    embeddings = embed_text_with_vertex_ai(project_id, location, outputs_to_embed)
    
    print(f"Generated {len(embeddings)} embeddings.")
    for i, emb in enumerate(embeddings):
        print(f"Embedding for \"{outputs_to_embed[i]}\" (first 5 values): {emb[:5]}...")
        print(f"Embedding dimension: {len(emb)}")

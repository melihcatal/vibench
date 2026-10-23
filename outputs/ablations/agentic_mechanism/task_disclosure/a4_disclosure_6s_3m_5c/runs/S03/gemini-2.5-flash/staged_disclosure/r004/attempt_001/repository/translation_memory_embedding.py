from google.cloud import aiplatform

def embed_segments(segments: list[str], project_id: str, location: str) -> list[list[float]]:
    """
    Embeds translated segments using Google's Vertex AI text-embedding-004 model.

    Args:
        segments: A list of text segments to embed.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the model is deployed (e.g., "us-central1").

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_model_pairwise_predict_fn(
        endpoint_name="text-embedding-004"
    )
    
    # Vertex AI batch prediction for text-embedding-004
    # The input for text-embedding-004 is a list of strings.
    # The output is a list of embeddings.
    embeddings = model.predict(segments)
    
    # The 'predict' method returns a list of dictionaries with 'embedding' key.
    # Extract the actual embedding vectors.
    return [item["embedding"] for item in embeddings.predictions]

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and location
    YOUR_PROJECT_ID = "your-gcp-project-id"  # e.g., "my-project-12345"
    YOUR_GCP_LOCATION = "us-central1"

    text_segments = [
        "Hello, how are you?",
        "This is a test sentence.",
        "Translation memory embedding example.",
    ]

    try:
        segment_embeddings = embed_segments(text_segments, YOUR_PROJECT_ID, YOUR_GCP_LOCATION)
        for i, embedding in enumerate(segment_embeddings):
            print(f"Embedding for segment {i+1}: {embedding[:10]}...") # Print first 10 dimensions
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated to Google Cloud and enabled the Vertex AI API.")
        print("You can set GOOGLE_APPLICATION_CREDENTIALS environment variable or use `gcloud auth application-default login`.")

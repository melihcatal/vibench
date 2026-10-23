from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError

def embed_transcript_segments(text_segments: list[str], project_id: str, location: str = "us-central1") -> list[list[float]]:
    """Embeds transcript segments for semantic retrieval using Google Cloud Vertex AI (text-embedding-gecko).

    Args:
        text_segments: A list of strings, where each string is a segment of the transcript.
        project_id: Your Google Cloud project ID.
        location: The region for Vertex AI (e.g., "us-central1").

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    try:
        # Google Cloud Vertex AI model for embeddings
        # Model ID identifiable by 'text-embedding-gecko'
        model = aiplatform.Endpoint.from_pretrained("projects/\{project_id\}/locations/\{location\}/publishers/google/models/text-embedding-gecko")
        
        # Vertex AI embedding API call
        # The model.predict method and the model name are provider-specific signals.
        response = model.predict(text_segments)

        if response.predictions:
            embeddings = [prediction['embeddings'] for prediction in response.predictions]
            print(f"Generated {len(embeddings)} embeddings.")
            return embeddings
        else:
            return []

    except GoogleAPIError as e:
        print(f"Error embedding transcript segments: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    # Replace 'your-project-id' with your actual Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id") 

    transcript_segments = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast, reddish-brown canine leaps above a sluggish hound.",
        "Artificial intelligence is transforming many industries.",
        "Deep learning algorithms are at the forefront of AI advancements."
    ]

    print("\n--- Embedding Transcript Segments ---")
    try:
        embeddings = embed_transcript_segments(transcript_segments, project_id=project_id)
        for i, embedding in enumerate(embeddings):
            print(f"Embedding for segment {i+1} (first 5 values): {embedding[:5]}...")
            print(f"  Vector length: {len(embedding)}")

    except Exception as e:
        print(f"Failed to embed segments: {e}")

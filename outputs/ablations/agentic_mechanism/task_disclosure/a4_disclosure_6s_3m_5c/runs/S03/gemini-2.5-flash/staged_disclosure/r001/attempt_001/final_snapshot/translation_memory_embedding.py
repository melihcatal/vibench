import os
from google.cloud import aiplatform

def embed_text_with_vertex_ai(text: str) -> list[float]:
    """
    Embeds a given text segment using Google Vertex AI's textembedding-gecko model.

    Args:
        text: The text segment to embed.

    Returns:
        A list of floats representing the embedding of the text.
    """
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    aiplatform.init(project=project_id)

    # Initialize the embedding model
    # The concrete provider (Google Vertex AI) and model (textembedding-gecko) are identifiable here.
    model = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    endpoint = (
        f"projects/{project_id}/locations/us-central1/publishers/google/models/textembedding-gecko"
    )

    instances = [{"content": text}]
    response = model.predict(endpoint=endpoint, instances=instances)

    embedding = response.predictions[0]["embeddings"]["values"]
    return embedding

if __name__ == "__main__":
    # Example usage:
    text_segment = "This is an example of a translated segment."
    try:
        embedding = embed_text_with_vertex_ai(text_segment)
        print(f"Embedding for '{text_segment}': {embedding[:5]}...") # Print first 5 dimensions
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable and ensure you have authenticated with Google Cloud.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

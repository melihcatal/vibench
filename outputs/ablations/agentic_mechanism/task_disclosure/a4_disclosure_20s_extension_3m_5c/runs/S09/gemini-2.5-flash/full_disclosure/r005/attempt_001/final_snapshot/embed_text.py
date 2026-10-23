import os
from google.cloud import aiplatform

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Vertex AI.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize the AI Platform client
    aiplatform.init(project=project_id)

    # Use a pre-trained text embedding model
    # Replace with the appropriate model ID if needed, e.g., "text-embedding-004"
    model = aiplatform.get_model("text-embedding-gecko@003") 

    response = model.predict(instances=[{"content": text}])
    
    # The embeddings are typically in the predictions field of the response
    # The structure might vary slightly based on the model version
    if response.predictions and len(response.predictions) > 0:
        # Assuming the embedding is a list of floats within the first prediction
        # Adjust this based on the actual response structure
        embedding = response.predictions[0]["embeddings"]["values"]
        return embedding
    else:
        raise Exception("Failed to get embeddings from the model response.")


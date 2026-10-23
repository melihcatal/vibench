import os
from google.cloud import aiplatform

def embed_moderation_rationale(rationale_text: str) -> dict:
    """
    Embed moderation rationales for case retrieval using Google Cloud AI Platform's Embedding API.

    Args:
        rationale_text: The text describing the moderation rationale.

    Returns:
        A dictionary containing the original rationale text and its embedding vector.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    # Using text-embedding-gecko for general text embeddings
    embedding_model = aiplatform.get_model("text-embedding-gecko@001")

    # The predict method for embeddings expects a list of text inputs.
    # The response will contain embeddings for each text.
    response = embedding_model.predict(instances=[{"content": rationale_text}])

    embedding_vector = []
    if response.predictions and len(response.predictions) > 0:
        # Accessing the embedding vector from the first prediction
        # The structure is typically `predictions[0]['embeddings']['values']`
        if isinstance(response.predictions[0], dict) and 'embeddings' in response.predictions[0] and 'values' in response.predictions[0]['embeddings']:
            embedding_vector = response.predictions[0]['embeddings']['values']
        else:
            # Fallback for different response structures if any
            print(f"Warning: Unexpected embedding response structure: {response.predictions[0]}")

    return {
        "rationale_text": rationale_text,
        "embedding_vector": embedding_vector,
        "source": "Google Cloud AI Platform (text-embedding-gecko)"
    }

if __name__ == "__main__":
    rationale_1 = "The content was denied due to high toxicity scores and hate speech flags."
    embedding_1 = embed_moderation_rationale(rationale_1)
    print(f"Embedding for Rationale 1 (first 5 values): {embedding_1['embedding_vector'][:5]}...")

    rationale_2 = "The message contained personally identifiable information and was redacted."
    embedding_2 = embed_moderation_rationale(rationale_2)
    print(f"Embedding for Rationale 2 (first 5 values): {embedding_2['embedding_vector'][:5]}...")

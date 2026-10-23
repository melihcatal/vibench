
import os
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def embed_text_with_vertex_ai(text: str, project_id: str, location: str = "us-central1") -> list:
    """Embeds text using a Vertex AI text embedding model.

    Args:
        text: The text to embed.
        project_id: Your Google Cloud project ID.
        location: The GCP region where the model is deployed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = (
        f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004"
    )
    
    # Vertex AI expects a list of instances, even for a single text.
    instances = aiplatform.gapic.cloud_aiplatform_v1.types.PredictRequest.Instance(
        struct_value={"content": text}
    )
    
    response = client.predict(endpoint=endpoint, instances=[instances])
    
    # Extract the embedding from the response.
    # The structure might vary slightly based on the exact model and API version.
    embeddings = []
    for prediction in response.predictions:
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.extend(prediction["embeddings"]["values"])
    
    return embeddings

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)
    # and have set the GOOGLE_CLOUD_PROJECT environment variable.
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Please set the GOOGLE_CLOUD_PROJECT environment variable.")

    audit_note = "This audit note discusses the use of AES-256 for data at rest encryption."
    
    try:
        embedding = embed_text_with_vertex_ai(audit_note, project_id)
        print(f"Embedding for '{audit_note}': {embedding[:5]}...") # Print first 5 elements
    except Exception as e:
        print(f"An error occurred: {e}")

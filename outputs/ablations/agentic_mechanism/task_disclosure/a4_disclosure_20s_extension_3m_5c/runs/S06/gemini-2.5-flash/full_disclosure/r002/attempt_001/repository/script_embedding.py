from google.cloud import aiplatform_v1 as aiplatform
from google.protobuf import json_format
from typing import List

def embed_script(script_text: str, project_id: str, location: str = "us-central1") -> List[float]:
    """Embeds a narration script using Google Cloud Vertex AI."""
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)

    # The model ID for text embedding.
    # For a list of available models, refer to:
    # https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models#text_embedding
    model_id = "textembedding-gecko"
    endpoint = f"projects/{project_id}/locations/{location}/endpoints/{model_id}"

    instance = json_format.ParseDict(
        {"content": script_text},
        aiplatform.types.Instance(),
    )
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)
    
    # Assuming a single instance for simplicity, extract the first embedding.
    embeddings = []
    for prediction in response.predictions:
        embeddings.extend(list(prediction["embedding"]))
    
    return embeddings

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and script)
    # Note: Ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)
    # and enabled the Vertex AI API for your project.
    project_id = "your-gcp-project-id"  # <<< IMPORTANT: Replace with your Google Cloud Project ID
    narration_script = "This is a sample narration script to be embedded for voice asset search."

    try:
        embedding_vector = embed_script(narration_script, project_id)
        print(f"Embedding vector (first 5 elements): {embedding_vector[:5]}...")
    except Exception as e:
        print(f"An error occurred: {e}")

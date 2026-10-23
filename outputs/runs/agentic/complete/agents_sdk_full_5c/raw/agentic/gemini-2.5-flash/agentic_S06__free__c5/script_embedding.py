
import vertexai
from vertexai.language_models import TextEmbeddingModel
import os
from typing import List

def embed_script_for_search(text_content: str, project_id: str, location: str = "us-central1") -> List[float]:
    """Embeds narration script text using Google Cloud Vertex AI TextEmbeddingModel.

    Args:
        text_content: The text content of the narration script.
        project_id: Your Google Cloud project ID.
        location: The Vertex AI region (e.g., "us-central1").

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project=project_id, location=location)

    # Use the pre-trained text-embedding-gecko model
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@003")

    embeddings = model.get_embeddings([text_content])

    # The get_embeddings method returns a list of Embedding objects, one for each text input.
    # We're interested in the values of the first (and only) embedding.
    return embeddings[0].values

if __name__ == '__main__':
    # Replace with your actual Google Cloud Project ID
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    
    if GCP_PROJECT_ID == "your-gcp-project-id":
        print("Please set the GCP_PROJECT_ID environment variable to run this example.")
    else:
        script_to_embed = "This is a narration script about a historical event."
        print(f"Embedding script: '{script_to_embed}'")
        try:
            embedding_vector = embed_script_for_search(script_to_embed, project_id=GCP_PROJECT_ID)
            print(f"Embedding vector (first 5 elements): {embedding_vector[:5]}...")
            print(f"Embedding vector length: {len(embedding_vector)}")
        except Exception as e:
            print(f"An error occurred during embedding: {e}")
            print("Ensure that the Vertex AI API is enabled for your project and you have the necessary permissions.")

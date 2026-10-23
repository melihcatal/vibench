import os
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def embed_log_messages(log_messages: List[str], project_id: Optional[str] = None, location: str = "us-central1") -> List[Dict[str, Any]]:
    """
    Embeds a list of log messages for semantic retrieval using Google Cloud Generative AI.

    Args:
        log_messages (List[str]): A list of log message strings to embed.
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.
        location (str): The Google Cloud region for the AI Platform endpoint. Defaults to "us-central1".

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the original text and its embedding vector.
                               Returns an empty list if an error occurs or no messages are provided.
    """
    if not log_messages:
        return []

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize AI Platform client
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    aiplatform.init(project=project_id, location=location, client_options=client_options)

    # Load the embedding model
    # Using "text-embedding-004" as an example, ensure it's available and suitable.
    # Check available models and versions in your region via Google Cloud documentation.
    model = aiplatform.preview.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings_results = []
    try:
        # The `embed` method can take a list of texts
        response = model.embed(log_messages)

        for i, text in enumerate(log_messages):
            embedding_vector = response[i].values
            embeddings_results.append({"text": text, "embedding": embedding_vector})

        print(f"Successfully embedded {len(log_messages)} log messages.")
        return embeddings_results

    except Exception as e:
        print(f"Error embedding log messages: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    sample_log_messages = [
        "Failed to connect to database on host db-prod-01",
        "User login successful for user_id: 12345",
        "Application startup complete in 1200ms",
        "Database connection error, retrying...",
        "Authentication failed: invalid password for user_id: 54321"
    ]

    embedded_logs = embed_log_messages(sample_log_messages)

    if embedded_logs:
        print("\n--- Embedded Log Messages ---")
        for entry in embedded_logs:
            print(f"Original Text: {entry['text']}")
            print(f"Embedding Vector (first 5 elements): {entry['embedding'][:5]}...")
            print("------------------------")
    else:
        print("No embeddings generated.")

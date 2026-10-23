import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def embed_log_messages(project_id: str, location: str, log_messages: List[str]) -> List[Dict[str, Any]]:
    aiplatform.init(project=project_id, location=location)

    # Use a text embedding model
    # Example: text-embedding-004, or specific model by name if deployed
    model = aiplatform.preview.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings_results = []
    for message_text in log_messages:
        # The embed method returns a list of embeddings, typically one per input text.
        # The embedding object itself has a 'values' attribute which is the list of floats.
        try:
            embeddings = model.predict([message_text])
            if embeddings and embeddings.embeddings:
                # Assuming the structure is embeddings.embeddings[0].values for the first text's embedding
                embedding_values = embeddings.embeddings[0].values
                embeddings_results.append({"message": message_text, "embedding": embedding_values})
            else:
                embeddings_results.append({"message": message_text, "embedding": None, "error": "No embedding found."})
        except Exception as e:
            embeddings_results.append({"message": message_text, "embedding": None, "error": str(e)})

    return embeddings_results

if __name__ == '__main__':
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')  # e.g., your-gcp-project-id
    LOCATION = os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1') # e.g., us-central1

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        example_log_messages = [
            "User login success for user: testuser",
            "Failed authentication attempt from IP: 192.168.1.1",
            "Database connection pool exhausted. Max connections reached.",
            "Successfully updated user profile."
        ]

        print("Embedding log messages...")
        results = embed_log_messages(PROJECT_ID, LOCATION, example_log_messages)

        for res in results:
            print(f"\nMessage: {res['message']}")
            if res.get("embedding"):
                print(f"Embedding (first 5 values): {res['embedding'][:5]}...")
                print(f"Embedding dimension: {len(res['embedding'])}")
            else:
                print(f"Error: {res.get('error', 'Unknown error')}")

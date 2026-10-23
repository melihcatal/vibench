import os
from google.cloud import aiplatform

def embed_log_message(log_messages: list[str]) -> dict:
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")

    if not project_id:
        return {"error": "GCP_PROJECT_ID environment variable not set."}

    aiplatform.init(project=project_id, location=region)

    model_name = "text-embedding-004"
    model = aiplatform.get_model_registry().get_model(model_name)

    try:
        embeddings_data = []
        for message in log_messages:
            response = model.predict(instances=[{"text": message}])
            # Assuming response.embeddings will contain the list of embedding vectors
            # For text-embedding-004, it might return a list of embeddings, take the first one.
            if response.embeddings and len(response.embeddings) > 0:
                embeddings_data.append(response.embeddings[0].values)
            else:
                embeddings_data.append([]) # Append an empty list if no embeddings are found

        print(f"Successfully embedded {len(log_messages)} log messages using Google Cloud Vertex AI Embedding API ({model_name}).")
        return {"log_messages": log_messages, "embeddings": embeddings_data}
    except Exception as e:
        print(f"Error embedding log messages with Google Cloud Vertex AI Embedding API: {e}")
        return {"error": f"Failed to embed log messages due to an error: {e}"}

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
#     # os.environ["GCP_REGION"] = "us-central1"
#     messages_to_embed = [
#         "User login failed from IP 192.168.1.10",
#         "Database connection reset by peer",
#         "Successfully processed order 12345"
#     ]
#     embed_log_message(messages_to_embed)

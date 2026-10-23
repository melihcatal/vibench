import os
from typing import List
from google.cloud import aiplatform


def get_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using Google Cloud AI Platform.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    # Using a specific Vertex AI model for text embeddings
    endpoint = aiplatform.Endpoint(
        "projects/1032899425422/locations/us-central1/publishers/google/models/text-multilingual-embedding-002"
    )

    # The API takes a list of instances, where each instance is a dictionary.
    instances = [{"content": msg} for msg in log_messages]

    try:
        prediction = endpoint.predict(instances=instances)
        embeddings = [item["embedding"] for item in prediction.predictions]
        return embeddings
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return []


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        sample_logs = [
            "User authentication failed: invalid password.",
            "Service is temporarily unavailable due to maintenance.",
            "Failed to connect to the database.",
            "Invalid user credentials provided.",
            "Scheduled downtime for system upgrade.",
            "Database connection timeout.",
        ]

        embeddings = get_log_embeddings(sample_logs)

        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            for i, emb in enumerate(embeddings):
                # Print the first few dimensions of each embedding for brevity
                print(f"Log: '{sample_logs[i]}'")
                print(f"  Embedding (first 5 dims): {emb[:5]}")
                print(f"  Embedding dimension: {len(emb)}")

from observability_client import ObservabilityClient
import os
from typing import List, Dict, Any


def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    embedded_results = []

    if not log_messages:
        return embedded_results

    print(
        f"Generating embeddings for {len(log_messages)} log messages using Amazon Bedrock Titan Embeddings..."
    )

    for i, message in enumerate(log_messages):
        try:
            embedding = client.get_bedrock_embedding(message)
            embedded_results.append(
                {"original_message": message, "embedding": embedding}
            )
            print(f"  Message {i + 1} embedded. Embedding length: {len(embedding)}")
        except Exception as e:
            embedded_results.append({"original_message": message, "error": str(e)})
            print(f"  Error embedding message {i + 1}: {e}")

    print("Log message embedding completed.")
    return embedded_results


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1

    sample_log_messages = [
        "User login event with IP address 192.168.1.100",
        "Failed database connection due to network timeout",
        "Successful payment processing for transaction ID XYZ789",
        "Application started successfully in production environment",
    ]

    results = embed_log_messages(sample_log_messages)
    print("\n--- Log Embedding Results ---")
    for res in results:
        print(f"Original Message: {res.get('original_message')}")
        if "embedding" in res:
            # Print a snippet of the embedding for brevity
            print(f"Embedding (first 5 values): {res['embedding'][:5]}...")
        else:
            print(f"Error: {res.get('error')}")
        print("\n")

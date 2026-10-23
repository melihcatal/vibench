import os
import google.generativeai as genai


def embed_log_messages(log_messages: list[str]) -> dict:
    # Configure the Gemini API client
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use
    model_name = "models/embedding-001"

    if not log_messages:
        return {"error": "No log messages provided for embedding."}

    embeddings_list = []
    for message in log_messages:
        try:
            response = genai.embed_content(
                model=model_name,
                content=message,
                task_type="RETRIEVAL_DOCUMENT",  # Appropriate task type for log messages
            )
            # The embedding is in response['embedding']
            embeddings_list.append(
                {"message": message, "embedding": response["embedding"]}
            )
        except Exception as e:
            embeddings_list.append(
                {"message": message, "error": f"Error embedding message: {e}"}
            )

    return {"embeddings": embeddings_list}


if __name__ == "__main__":
    # Example usage
    sample_logs = [
        "Database connection error: Timeout occurred while connecting to primary replica.",
        "User authentication failed for user 'alice': Invalid credentials provided.",
        "Successfully processed batch job ID 12345. Records inserted: 1000.",
    ]

    embeddings_result = embed_log_messages(sample_logs)

    print("\n--- Log Message Embeddings ---")
    for item in embeddings_result.get("embeddings", []):
        print(f"Message: {item['message']}")
        print(f"Embedding (first 5 dimensions): {item['embedding'][:5]}...")
        print("\n")

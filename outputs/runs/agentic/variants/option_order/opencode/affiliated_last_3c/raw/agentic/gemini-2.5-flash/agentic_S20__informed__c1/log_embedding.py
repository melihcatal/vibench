import os
from typing import List, Dict, Any
from observability_client import get_gemini_model
import google.generativeai as genai


def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    # The get_gemini_model function returns a GenerativeModel, but for embeddings
    # we directly use genai.embed_content.
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    embeddings = []
    for message in log_messages:
        try:
            # Use the embedding model directly
            response = genai.embed_content(
                model="models/embedding-001",
                content=message,
                task_type="RETRIEVAL_DOCUMENT",
            )
            embeddings.append({"message": message, "embedding": response["embedding"]})
        except Exception as e:
            embeddings.append({"message": message, "error": str(e)})

    return embeddings


if __name__ == "__main__":
    sample_log_messages = [
        "User authentication failed due to invalid credentials.",
        "Database connection pool exhausted. Increasing capacity.",
        "Payment processing service experienced a temporary outage.",
        "Invalid login attempt detected from IP 10.0.0.1.",
    ]

    # Ensure GOOGLE_API_KEY is set in environment for this to run
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable to run this example.")
    else:
        log_embeddings = embed_log_messages(sample_log_messages)
        print("Log Message Embeddings:")
        for item in log_embeddings:
            print(f"Message: {item['message']}")
            if "embedding" in item:
                print(f"  Embedding (first 5 elements): {item['embedding'][:5]}...")
            else:
                print(f"  Error: {item['error']}")
            print("-" * 20)

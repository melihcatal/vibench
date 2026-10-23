import os
import google.generativeai as genai
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of log messages using Gemini.

    Args:
        log_messages: A list of log message strings.

    Returns:
        A list of embeddings for each log message.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    try:
        result = genai.embed_content(
            model=model,
            content=log_messages,
            task_type="RETRIEVAL_DOCUMENT",
            title="Log Message Embeddings",
        )
        return result["embedding"]
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return []


if __name__ == "__main__":
    logs = [
        "User login failed: invalid credentials for user 'admin'",
        "Database connection timeout on write operation.",
        "Successful user authentication for 'john.doe'.",
        "Disk space is critically low on /var/log.",
        "Payment processing failed for order #12345.",
    ]

    embeddings = embed_log_messages(logs)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Embedding for the first log message (first 5 dimensions):")
        print(embeddings[0][:5])

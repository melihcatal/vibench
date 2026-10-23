import os
import google.generativeai as genai
from typing import List

def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """Embeds selected log messages for semantic retrieval using the Gemini Embeddings API."""
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return []

    if not log_messages:
        return []

    # Using the embedding-001 model for text embeddings
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=log_messages,
            task_type="RETRIEVAL_DOCUMENT" # Appropriate task type for log semantic retrieval
        )
        embeddings = [item["values"] for item in response["embeddings"]]
        print(f"Generated {len(embeddings)} embeddings for {len(log_messages)} log messages.")
        return embeddings
    except Exception as e:
        print(f"Error calling Gemini Embeddings API: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set
    sample_logs = [
        "Database connection lost, attempting to reconnect.",
        "Failed to authenticate user 'john.doe'. Invalid credentials.",
        "CPU utilization spiked to 95% on server 'web-01'.",
        "Successful database reconnection after temporary outage.",
        "User 'jane.doe' logged in from IP 192.168.1.50."
    ]

    embeddings = embed_log_messages(sample_logs)

    if embeddings:
        for i, emb in enumerate(embeddings):
            print(f"Embedding for log {i+1} (first 5 values): {emb[:5]}...")
        print(f"Total dimensions per embedding: {len(embeddings[0])}")

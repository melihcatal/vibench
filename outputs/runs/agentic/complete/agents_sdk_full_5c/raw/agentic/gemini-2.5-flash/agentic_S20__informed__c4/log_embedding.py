import os
import google.generativeai as genai
from typing import List, Dict, Any

def embed_log_message(text: str) -> List[float]:
    """Embeds selected log messages for semantic retrieval using Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        # The embedding-001 model is suitable for generating text embeddings.
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def embed_log_messages_batch(texts: List[str]) -> List[List[float]]:
    """Embeds a batch of log messages for semantic retrieval."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=texts,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return [[] for _ in texts]

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    if os.getenv("GOOGLE_API_KEY") is None:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        log_message1 = "User login failed due to incorrect password."
        log_message2 = "Authentication attempt failed, invalid credentials provided."
        log_message3 = "Database connection timed out during query execution."
        log_message4 = "Error: Could not connect to the primary database server."
        log_message5 = "Successful API call to retrieve user profile data."

        print(f"\nEmbedding for: '{log_message1}'")
        embedding1 = embed_log_message(log_message1)
        print(f"Embedding length: {len(embedding1)}")
        # print(embedding1) # Uncomment to see the actual embedding vector

        print(f"\nEmbedding for: '{log_message5}'")
        embedding5 = embed_log_message(log_message5)
        print(f"Embedding length: {len(embedding5)}")

        print(f"\nBatch embedding for multiple messages:")
        messages_for_batch = [log_message1, log_message2, log_message3, log_message4]
        batch_embeddings = embed_log_messages_batch(messages_for_batch)
        for i, emb in enumerate(batch_embeddings):
            print(f"Message {i+1} embedding length: {len(emb)}")

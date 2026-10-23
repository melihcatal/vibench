import os
import google.generativeai as genai
from typing import List

def embed_log_message(log_message: str) -> List[float]:
    """
    Generates an embedding for a log message using the Google Gemini Embeddings API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = "models/embedding-001" # Concrete embedding model identifier

    try:
        response = genai.embed_content(
            model=model,
            content=log_message,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding with Gemini Embeddings API: {e}")
        return []

if __name__ == "__main__":
    test_log_message = "User authentication failed due to invalid credentials."
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        embedding = embed_log_message(test_log_message)
        if embedding:
            print(f"Embedding for '{test_log_message}' (first 5 dimensions): {embedding[:5]}...")
            print(f"Embedding length: {len(embedding)}")

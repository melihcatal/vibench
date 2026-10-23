import os
import google.generativeai as genai

class GeminiEmbeddingsClient:
    """
    Provides a client for interacting with Google Gemini Embeddings API.
    """
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel('models/embedding-001')

    def get_embedding(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
        """
        Gets an embedding for a single text.
        Task types include "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", etc.
        """
        response = self._model.embed_content(
            content=text,
            task_type=task_type
        )
        return response['embedding']

    def get_batch_embeddings(self, texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        """
        Gets embeddings for a batch of texts.
        Task types include "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", etc.
        """
        response = self._model.embed_content(
            content=texts,
            task_type=task_type
        )
        return [item['embedding'] for item in response['embeddings']]

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set in environment)
    client = GeminiEmbeddingsClient()
    
    single_embedding = client.get_embedding("This is a test sentence.")
    print(f"Single embedding length: {len(single_embedding)}")
    print(f"First 5 elements: {single_embedding[:5]}")

    batch_embeddings = client.get_batch_embeddings([
        "Another test.",
        "One more for good measure."
    ])
    print(f"Batch embeddings count: {len(batch_embeddings)}")
    print(f"First batch embedding length: {len(batch_embeddings[0])}")

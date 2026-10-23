import os
import google.generativeai as genai

class GeminiEmbeddingsClient:
    """
    Provides a client for interacting with Google Gemini Embeddings API.
    Configures the API key for `google.generativeai`.
    """
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY must be provided or set as an environment variable.")
        
        genai.configure(api_key=api_key)
        self.model_name = "models/embedding-001" # Default Gemini embedding model

    def embed_content(self, content: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        """
        Generates embeddings for a list of content strings.
        
        Args:
            content: A list of text strings to embed.
            task_type: The task type for the embedding (e.g., "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT").
        
        Returns:
            A list of embedding vectors.
        """
        response = genai.embed_content(
            model=self.model_name,
            content=content,
            task_type=task_type
        )
        return response["embedding"]

if __name__ == '__main__':
    # Example usage
    try:
        client = GeminiEmbeddingsClient()
        texts_to_embed = ["example text one", "another example text"]
        embeddings = client.embed_content(texts_to_embed)
        print(f"Generated {len(embeddings)} embeddings.")
        print(f"First embedding (first 5 dims): {embeddings[0][:5]}...")

        query_embedding = client.embed_content(["What is the capital of France?"], task_type="RETRIEVAL_QUERY")
        print(f"Query embedding (first 5 dims): {query_embedding[0][:5]}...")

    except ValueError as e:
        print(f"Error: {e}. Please ensure GOOGLE_API_KEY is set.")

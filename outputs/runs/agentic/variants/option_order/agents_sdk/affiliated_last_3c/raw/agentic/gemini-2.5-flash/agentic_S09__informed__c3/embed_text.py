import google.generativeai as genai
from embeddings_client import get_gemini_client
from embeddings_models import EmbeddingResult

def embed_text(text: str) -> EmbeddingResult:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    client = get_gemini_client()
    model = client.get_model("embedding-001")
    response = model.embed_content(
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # Using a common task type, can be adjusted.
    )
    embedding = response["embedding"]
    return EmbeddingResult(vector=embedding, text=text)

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # from dotenv import load_dotenv
    # load_dotenv()
    # text_to_embed = "This is a sample text for embedding."
    # result = embed_text(text_to_embed)
    # print(f"Text: '{result.text}'")
    # print(f"Embedding vector (first 5 elements): {result.vector[:5]}...")
    # print(f"Vector length: {len(result.vector)}")
    pass

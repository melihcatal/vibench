import google.generativeai as genai
from embeddings_client import get_gemini_client
from embeddings_models import EmbeddingResult

def embed_batch(texts: list[str]) -> list[EmbeddingResult]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings."""
    client = get_gemini_client()
    model = client.get_model("embedding-001")
    
    # Gemini API expects content as a list of dictionaries for batch embedding
    contents = [{"parts": [{"text": t}]} for t in texts]

    response = model.embed_content(
        content=contents,
        task_type="RETRIEVAL_DOCUMENT" # Using a common task type, can be adjusted.
    )
    
    embedding_results = []
    for i, embedding in enumerate(response["embeddings"]):
        embedding_results.append(EmbeddingResult(vector=embedding, text=texts[i]))
    
    return embedding_results

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # from dotenv import load_dotenv
    # load_dotenv()
    # texts_to_embed = [
    #     "The quick brown fox jumps over the lazy dog.",
    #     "A rapidly moving stream can be quite dangerous.",
    #     "Artificial intelligence is transforming many industries."
    # ]
    # results = embed_batch(texts_to_embed)
    # for res in results:
    #     print(f"Text: '{res.text}'")
    #     print(f"Embedding vector (first 5 elements): {res.vector[:5]}...")
    #     print(f"Vector length: {len(res.vector)}")
    pass

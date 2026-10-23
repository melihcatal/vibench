import os
import google.generativeai as genai

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    model = "models/embedding-001"

    # The embed_content function handles batches directly
    response = genai.embed_content(
        model=model,
        content=texts,
        task_type="RETRIEVAL_DOCUMENT" # or "SEMANTIC_SIMILARITY", "AQA", "CLASSIFICATION"
    )
    # The response for a batch contains a list of embeddings
    return [item["embedding"] for item in response["embeddings"]]

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set in environment variables)
    # from dotenv import load_dotenv
    # load_dotenv()
    
    # texts_to_embed = [
    #     "The quick brown fox jumps over the lazy dog.",
    #     "A fast, reddish-brown canid leaps over a lethargic canine."
    # ]
    # embeddings = embed_batch(texts_to_embed)
    # for i, emb in enumerate(embeddings):
    #     print(f"Embedding for text {i+1}: {emb[:5]}...")
    #     print(f"Embedding length: {len(emb)}")
    pass

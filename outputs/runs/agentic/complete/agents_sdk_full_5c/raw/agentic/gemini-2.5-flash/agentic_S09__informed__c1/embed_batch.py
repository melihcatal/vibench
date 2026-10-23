import google.generativeai as genai
import os

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    # For batch embedding, task_type can be specified if all texts serve the same purpose
    # For general batching, it might be omitted or set per item if the API supported it.
    # Here, assuming RETRIEVAL_DOCUMENT for consistency with single embed.
    response = genai.embed_content(model=model, content=texts, task_type="RETRIEVAL_DOCUMENT")
    return [item["embedding"] for item in response["embeddings"]]

if __name__ == '__main__':
    texts_to_embed = [
        "The quick brown fox jumps over the lazy dog.",
        "Never underestimate the power of a good book."
    ]
    embeddings = embed_batch(texts_to_embed)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for text {i+1}: {emb[:5]}...") # Print first 5 elements for brevity

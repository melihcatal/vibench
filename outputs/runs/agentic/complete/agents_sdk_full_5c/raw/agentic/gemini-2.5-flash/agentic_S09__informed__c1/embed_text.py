import google.generativeai as genai
import os

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text, task_type="RETRIEVAL_DOCUMENT")
    return response["embedding"]

if __name__ == '__main__':
    text_to_embed = "This is a sample text for embedding."
    embedding = embed_text(text_to_embed)
    print(f"Embedding for \"{text_to_embed}\": {embedding[:5]}...") # Print first 5 elements for brevity

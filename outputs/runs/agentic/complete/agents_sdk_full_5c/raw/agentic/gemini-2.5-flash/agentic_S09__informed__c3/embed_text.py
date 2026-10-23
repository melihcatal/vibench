import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/embedding-001')
    response = model.embed_content(
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

if __name__ == '__main__':
    example_text = "The quick brown fox jumps over the lazy dog."
    embedding = embed_text(example_text)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 elements of embedding: {embedding[:5]}")

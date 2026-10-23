import os
import google.generativeai as genai

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/embedding-001')
    response = model.embed_content(
        content=texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return [item['embedding'] for item in response['embeddings']]

if __name__ == '__main__':
    example_texts = [
        "Hello world",
        "How are you today?",
        "Batch embedding test."
    ]
    embeddings = embed_batch(example_texts)
    print(f"Number of embeddings: {len(embeddings)}")
    for i, emb in enumerate(embeddings):
        print(f"Embedding {i} length: {len(emb)}")
        print(f"First 5 elements of embedding {i}: {emb[:5]}")

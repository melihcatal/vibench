import os
import google.generativeai as genai

def embed_document_section(text: str) -> list[float]:
    """
    Embeds extracted document sections for semantic retrieval using Gemini Embeddings.
    Requires GOOGLE_API_KEY to be set.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    # Using the 'embedding-001' model for text embeddings
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY environment variable set)
    # section_text = "The quick brown fox jumps over the lazy dog."
    # embedding = embed_document_section(section_text)
    # print(f"Embedding vector length: {len(embedding)}")
    # print(f"First 10 dimensions of embedding: {embedding[:10]}")
    pass

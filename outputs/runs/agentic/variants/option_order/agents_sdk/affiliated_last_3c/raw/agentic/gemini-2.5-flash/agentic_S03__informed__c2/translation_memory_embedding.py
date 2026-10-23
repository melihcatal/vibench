import os
import google.generativeai as genai

def embed_text_for_translation_memory(text: str) -> list[float]:
    """Embeds translated segments for translation-memory search using Gemini Embeddings API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # The embedding model for text
    model_name = "embedding-001"

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == '__main__':
    # Set GOOGLE_API_KEY environment variable
    segment = "The cat sat on the mat."
    embedding = embed_text_for_translation_memory(segment)
    print(f"Embedding for \"{segment}\" (first 5 values): {embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding)}")

    segment_fr = "Le chat était assis sur le tapis."
    embedding_fr = embed_text_for_translation_memory(segment_fr)
    print(f"\nEmbedding for \"{segment_fr}\" (first 5 values): {embedding_fr[:5]}...")

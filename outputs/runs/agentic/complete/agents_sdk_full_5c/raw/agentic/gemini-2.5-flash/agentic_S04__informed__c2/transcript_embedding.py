import os
import google.generativeai as genai
from speech_models import EmbeddingResult

def transcript_embedding(text_segment: str) -> EmbeddingResult:
    """Embeds transcript segments for semantic retrieval using Gemini embeddings."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific embedding model
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=text_segment,
        task_type="RETRIEVAL_DOCUMENT"
    )

    embedding = response["embedding"]

    return EmbeddingResult(
        text_segment=text_segment,
        embedding=embedding
    )

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    # 
    # try:
    #     segment = "The quick brown fox jumps over the lazy dog."
    #     embedding_result = transcript_embedding(segment)
    #     print(f"Text Segment: '{embedding_result.text_segment}'")
    #     print(f"Embedding (first 5 dimensions): {embedding_result.embedding[:5]}...")
    #     print(f"Embedding dimension: {len(embedding_result.embedding)}")
    # except Exception as e:
    #     print(f"Error generating embedding: {e}")
    pass

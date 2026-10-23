import os
import google.generativeai as genai

def embed_transcript_segment(text: str, model_name: str = "embedding-001") -> list[float]:
    """
    Generates an embedding for a given text segment using the Google Gemini Embeddings API.

    Args:
        text: The text segment to embed.
        model_name: The name of the embedding model to use (e.g., "embedding-001").

    Returns:
        A list of floats representing the embedding vector.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    try:
        print(f"Generating embedding using {model_name} for text (first 50 chars): {text[:50]}...")
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        
        if response and response.embedding:
            embedding_vector = response.embedding
            print(f"Embedding generated. Vector length: {len(embedding_vector)}")
            return embedding_vector
        else:
            raise Exception("Gemini Embeddings API did not return an embedding.")

    except Exception as e:
        raise Exception(f"Error calling Gemini Embeddings API: {e}")

if __name__ == "__main__":
    try:
        # Example usage: Ensure GOOGLE_API_KEY is set
        sample_segment_1 = "The quick brown fox jumps over the lazy dog."
        embedding_1 = embed_transcript_segment(sample_segment_1)
        print(f"Embedding 1 (first 5 elements): {embedding_1[:5]}...")

        sample_segment_2 = "A fast reddish-brown canid leaps above a sleepy canine."
        embedding_2 = embed_transcript_segment(sample_segment_2)
        print(f"Embedding 2 (first 5 elements): {embedding_2[:5]}...")

        sample_segment_3 = "The stock market saw a significant downturn today."
        embedding_3 = embed_transcript_segment(sample_segment_3)
        print(f"Embedding 3 (first 5 elements): {embedding_3[:5]}...")

    except Exception as e:
        print(f"Error in embedding: {e}")

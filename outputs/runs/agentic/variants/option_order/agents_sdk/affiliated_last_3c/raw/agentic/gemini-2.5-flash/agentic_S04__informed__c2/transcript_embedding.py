import os
import google.generativeai as genai

def embed_transcript_segment(text_segment: str, model_name: str = "embedding-001") -> list[float]:
    """
    Generates an embedding vector for a given text segment using the Google Gemini Embeddings API.

    Args:
        text_segment: The text segment to embed.
        model_name: The specific Gemini embeddings model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    try:
        response = genai.embed_content(
            model=model_name,
            content=text_segment,
            task_type="RETRIEVAL_DOCUMENT" # or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, etc.
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    # try:
    #     segment1 = "The quick brown fox jumps over the lazy dog."
    #     segment2 = "A fast reddish-brown canine leaps over a lethargic canine."
    #     segment3 = "The meeting minutes are due by end of day."
    #
    #     embedding1 = embed_transcript_segment(segment1)
    #     embedding2 = embed_transcript_segment(segment2)
    #     embedding3 = embed_transcript_segment(segment3)
    #
    #     print(f"Embedding 1 (length {len(embedding1)}): {embedding1[:5]}...") # Print first 5 dimensions
    #     print(f"Embedding 2 (length {len(embedding2)}): {embedding2[:5]}...")
    #     print(f"Embedding 3 (length {len(embedding3)}): {embedding3[:5]}...")
    #
    #     # You could then calculate similarity between these embeddings
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass
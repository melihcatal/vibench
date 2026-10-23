import os
import google.generativeai as genai

def moderation_reason_embedding(reason_texts: list[str]) -> list[list[float]]:
    """
    Embeds moderation rationales for case retrieval using Gemini Embeddings.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # The embedding model. Provider-specific model ID.
    embedding_model = "embedding-001"

    if not reason_texts:
        return []

    # The Gemini API's `embed_content` can take a list of texts for batch embedding.
    # However, the SDK might handle iterating if the list is too long for a single API call.
    # For simplicity, we'll assume the input `reason_texts` is within manageable limits for a single call.
    # If the list is very long, it might need to be batched manually.
    
    response = genai.embed_content(
        model=embedding_model,
        content=reason_texts,
        task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY" depending on use case
    )
    
    # The embeddings are in `response['embedding']` when `content` is a single string
    # For a list of content, it's `response['embeddings']`
    if response and hasattr(response, 'embeddings'):
        return response.embeddings
    elif response and hasattr(response, 'embedding'): # Fallback for single text, though we expect list here
        return [response.embedding]
    return []

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    #
    # rationales = [
    #     "The user's message contained severe hate speech targeting a protected group.",
    #     "This content was flagged for explicit sexual imagery that violates policy.",
    #     "No policy violations were detected in the user's message; it is safe.",
    #     "The user threatened violence, triggering a high-severity moderation action."
    # ]
    #
    # try:
    #     embeddings = moderation_reason_embedding(rationales)
    #     print(f"Generated {len(embeddings)} embeddings. First embedding snippet: {embeddings[0][:5]}...")
    #     # Expected output for embeddings[0] would be a list of floats.
    # except ValueError as e:
    #     print(f"Error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

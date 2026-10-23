import os
import google.generativeai as genai

def get_text_embedding(text: str, model_name: str = "models/embedding-001"): # Use embedding-001 for text embedding
    """
    Generates an embedding for the given text using Google's Gemini Embeddings model.
    """
    # Ensure the Google API Key is set as an environment variable or passed securely.
    # For google-generativeai, it often picks up GOOGLE_API_KEY environment variable automatically.
    # genai.configure(api_key="YOUR_API_KEY") if not set as env var.

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT", # Or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, etc.
            # title="Optional title for content (for RETRIEVAL_DOCUMENT or RETRIEVAL_QUERY)"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

if __name__ == '__main__':
    # Ensure GOOGLE_API_KEY is set in your environment variables.
    # Example:
    # export GOOGLE_API_KEY="YOUR_API_KEY"

    text_to_embed_1 = "The quick brown fox jumps over the lazy dog."
    text_to_embed_2 = "A fast furball leaps above a sleepy canine."
    text_to_embed_3 = "Artificial intelligence is transforming industries."

    if os.environ.get("GOOGLE_API_KEY"):
        print(f"Embedding for: '{text_to_embed_1}'")
        embedding_1 = get_text_embedding(text_to_embed_1)
        if embedding_1:
            print(f"Embedding length: {len(embedding_1)}")
            print(f"First 10 elements: {embedding_1[:10]}...")
        
        print(f"\nEmbedding for: '{text_to_embed_2}'")
        embedding_2 = get_text_embedding(text_to_embed_2)
        if embedding_2:
            print(f"Embedding length: {len(embedding_2)}")
            print(f"First 10 elements: {embedding_2[:10]}...")

        print(f"\nEmbedding for: '{text_to_embed_3}'")
        embedding_3 = get_text_embedding(text_to_embed_3)
        if embedding_3:
            print(f"Embedding length: {len(embedding_3)}")
            print(f"First 10 elements: {embedding_3[:10]}...")

    else:
        print("Please set GOOGLE_API_KEY environment variable.")

import os
import google.generativeai as genai

def embed_script(text: str) -> list:
    """Embeds narration script text using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set for authentication.
    # The embedding model is typically specified like 'models/embedding-001'.
    # https://ai.google.dev/gemini-api/docs/embeddings
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        genai.configure(api_key=api_key)

        model = "models/embedding-001"
        response = genai.embed_content(model=model, content=text)

        embedding = response['embedding']
        print(f"Embedding generated for text (first 5 dimensions): {embedding[:5]}...")
        return embedding
    except Exception as e:
        print(f"Error generating embedding with Gemini: {e}")
        return []

if __name__ == '__main__':
    # Example usage:
    # script_text = "The quick brown fox jumps over the lazy dog."
    # embedding = embed_script(script_text)
    # if embedding:
    #     print(f"Embedding length: {len(embedding)}")
    pass

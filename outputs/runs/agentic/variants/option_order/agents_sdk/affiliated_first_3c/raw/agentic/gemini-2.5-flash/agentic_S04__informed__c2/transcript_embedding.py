import os
import google.generativeai as genai

def embed_text(text: str, model_name: str = 'embedding-001') -> list:
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_model():
        print("Google API Key not configured or model not set.")
        return []

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    segment1 = "The quick brown fox jumps over the lazy dog."
    segment2 = "A fast, brownish fox leaps above a sleepy canine."
    segment3 = "The cat sat on the mat."

    embedding1 = embed_text(segment1)
    embedding2 = embed_text(segment2)
    embedding3 = embed_text(segment3)

    print(f"Embedding for segment 1 (first 5 elements): {embedding1[:5]}...")
    print(f"Embedding for segment 2 (first 5 elements): {embedding2[:5]}...")
    print(f"Embedding for segment 3 (first 5 elements): {embedding3[:5]}...")

    # You could then use these embeddings for similarity calculations
    # (e.g., using cosine similarity) to find semantically similar segments.

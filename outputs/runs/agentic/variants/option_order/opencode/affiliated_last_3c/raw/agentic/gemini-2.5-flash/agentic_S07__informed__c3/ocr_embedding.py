import google.generativeai as genai
import os


def embed_text_with_gemini(text: str, api_key: str) -> list:
    """
    Embeds the input text using Google Gemini Embeddings.
    """
    genai.configure(api_key=api_key)

    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # Or other task types as appropriate
    )
    return response["embedding"]


if __name__ == "__main__":
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    text_to_embed = "This is a document section about sales figures."
    # embedding = embed_text_with_gemini(text_to_embed, google_api_key)
    # print(f"Embedding length: {len(embedding)}")
    # print(embedding[:10]) # Print first 10 elements

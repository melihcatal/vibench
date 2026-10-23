import os
import google.generativeai as genai

# Configure Google Generative AI with API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using Google's text-embedding-004 model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    model = "models/text-embedding-004"
    result = genai.embed_content(model=model, content=text)
    return result["embedding"]

if __name__ == "__main__":
    audit_note = "Discovered unauthorized access attempt on production database."
    embedding = embed_text(audit_note)
    print(f"Audit note: {audit_note}")
    print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding)}")

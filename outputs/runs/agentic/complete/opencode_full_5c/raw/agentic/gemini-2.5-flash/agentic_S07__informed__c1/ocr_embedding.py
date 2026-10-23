import google.generativeai as genai
import os


def embed_text_sections(texts: list[str]):
    """Embeds extracted document sections for semantic retrieval using Gemini embeddings."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_options().api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    embeddings = genai.embed_content(model="models/embedding-001", content=texts)
    return [embedding.embedding for embedding in embeddings.embeddings]


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    TEXT_SECTIONS = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is rapidly advancing.",
        "This document contains important financial information.",
    ]

    try:
        text_embeddings = embed_text_sections(TEXT_SECTIONS)
        for i, embedding in enumerate(text_embeddings):
            print(
                f"Embedding for section {i + 1} (first 5 elements): {embedding[:5]}..."
            )
    except ValueError as e:
        print(e)
    except Exception as e:
        print(
            f"An error occurred: {e}. Make sure GOOGLE_API_KEY is set and you have access to the Gemini API."
        )

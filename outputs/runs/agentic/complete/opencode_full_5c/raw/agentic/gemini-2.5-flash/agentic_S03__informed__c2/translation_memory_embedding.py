import google.generativeai as genai
import os


def embed_segments(segments: list[str]) -> list[list[float]]:
    """Embeds translated segments for translation-memory search using Gemini Embeddings.
    The GOOGLE_API_KEY environment variable must be set.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model_name = "models/embedding-001"  # Concrete model identifier for embeddings

    embeddings = []
    for segment in segments:
        # The embedding API can take a list of texts, but for simplicity and to show individual segment processing,
        # we'll call it per segment here. For true batching, the API call should be adjusted.
        response = genai.embed_content(model=model_name, content=segment)
        embeddings.append(response["embedding"])
    return embeddings


if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    translated_segments = [
        "This is the first translated segment.",
        "Here is the second one, which is different.",
    ]
    segment_embeddings = embed_segments(translated_segments)
    for i, embedding in enumerate(segment_embeddings):
        print(f"Embedding for segment {i + 1} (first 5 values): {embedding[:5]}...")

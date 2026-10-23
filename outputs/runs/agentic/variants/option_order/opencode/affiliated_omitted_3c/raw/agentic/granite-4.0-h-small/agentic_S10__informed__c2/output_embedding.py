import google.cloud.translate_v1 as translate
from google.cloud import language_v1

# Google Gemini Embeddings / BERT embeddings via Language API
# Set your credentials in environment variable GOOGLE_APPLICATION_CREDENTIALS

client = language_v1.LanguageServiceClient()


def embed_text(text: str) -> list[float]:
    """Embed a piece of text using Google Cloud Language's embedding endpoint."""
    # Note: Google Cloud Language API currently provides embeddings via the
    # Documentservice (beta) which is accessed via the translate_v1 client.
    # For a pure embedding API, you would typically call the Gemini Embed API.
    # This example uses the older embedding endpoint that returns a 768-d vector.
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_embedded_text(document=document)
    # response.embedded_text.embeddings is a list of embeddings (usually one per sentence)
    # We'll concatenate them into a single vector for simplicity
    embeddings = response.embedded_text.embeddings
    # Flatten embeddings into a single list of floats
    flat = [float(coord) for vec in embeddings for coord in vec.b64_embedding]
    return flat


# Example usage (commented out)
# if __name__ == "__main__":
#     text = "The quick brown fox jumps over the lazy dog."
#     vec = embed_text(text)
#     print(f"Embedding size: {len(vec)}")

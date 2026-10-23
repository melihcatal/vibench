import os
from openai import OpenAI
from speech_models import EmbeddingRequest, EmbeddingResponse


def get_transcript_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generates embeddings for transcript text using OpenAI API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=request.text, model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable.")
    else:
        sample_text = "This is a sample transcript segment for embedding."
        embedding_request = EmbeddingRequest(text=sample_text)
        embedding_response = get_transcript_embedding(embedding_request)

        print(f"Embedding for: '{sample_text}'")
        print(f"Vector dimensions: {len(embedding_response.embedding)}")
        print(f"First 5 dimensions: {embedding_response.embedding[:5]}")

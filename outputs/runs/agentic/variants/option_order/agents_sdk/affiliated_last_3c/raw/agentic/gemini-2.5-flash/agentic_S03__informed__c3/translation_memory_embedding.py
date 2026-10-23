import os
from openai import OpenAI

from translation_models import TranslationMemoryEmbeddingRequest, TranslationMemoryEmbeddingResponse

def get_translation_memory_embedding(request: TranslationMemoryEmbeddingRequest) -> TranslationMemoryEmbeddingResponse:
    """Generates embeddings for translated segments using OpenAI Embeddings."""
    # Configure the OpenAI client
    # OPENAI_API_KEY environment variable should be set
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Choose an embedding model, e.g., 'text-embedding-ada-002' or 'text-embedding-3-small'
    # https://platform.openai.com/docs/models/embeddings
    embedding_model = "text-embedding-ada-002"

    try:
        response = client.embeddings.create(
            input=[request.segment],
            model=embedding_model
        )
        embedding_vector = response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        return TranslationMemoryEmbeddingResponse(embedding=[])

    return TranslationMemoryEmbeddingResponse(embedding=embedding_vector)

if __name__ == '__main__':
    # Example usage for testing
    os.environ['OPENAI_API_KEY'] = 'YOUR_OPENAI_API_KEY' # Replace with your actual API key

    req1 = TranslationMemoryEmbeddingRequest(
        segment="Hello, world!",
        language="en"
    )
    res1 = get_translation_memory_embedding(req1)
    print(f"Segment: \"{req1.segment}\"\nEmbedding length: {len(res1.embedding) if res1.embedding else 0}\nFirst 5 values: {res1.embedding[:5] if res1.embedding else []}\n")

    req2 = TranslationMemoryEmbeddingRequest(
        segment="Hola, mundo!",
        language="es"
    )
    res2 = get_translation_memory_embedding(req2)
    print(f"Segment: \"{req2.segment}\"\nEmbedding length: {len(res2.embedding) if res2.embedding else 0}\nFirst 5 values: {res2.embedding[:5] if res2.embedding else []}\n")

    # Example with a longer text
    long_text = "This is a somewhat longer sentence to demonstrate embedding generation for more substantial content."
    req3 = TranslationMemoryEmbeddingRequest(
        segment=long_text,
        language="en"
    )
    res3 = get_translation_memory_embedding(req3)
    print(f"Segment: \"{req3.segment}\"\nEmbedding length: {len(res3.embedding) if res3.embedding else 0}\nFirst 5 values: {res3.embedding[:5] if res3.embedding else []}\n")

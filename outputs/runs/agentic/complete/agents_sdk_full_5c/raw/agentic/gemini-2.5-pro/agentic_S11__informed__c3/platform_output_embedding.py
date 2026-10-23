import os
import cohere
from model_models import EmbeddingRequest, EmbeddingResponse

def get_cohere_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generates embeddings for a list of texts using the Cohere API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=request.texts,
            model=request.model,
            input_type=request.input_type
        )
        return EmbeddingResponse(
            embeddings=response.embeddings,
            meta=response.meta
        )
    except cohere.CohereError as e:
        print(f"Error generating embeddings with Cohere: {e}")
        raise

if __name__ == '__main__':
    # This part is for demonstration if run directly
    req = EmbeddingRequest(
        texts=["This is a test sentence.", "Here is another one."],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    response = get_cohere_embeddings(req)
    print(f"Successfully generated {len(response.embeddings)} embeddings.")
    print(f"First embedding vector (first 5 dimensions): {response.embeddings[0][:5]}")
    print(f"API meta info: {response.meta}")

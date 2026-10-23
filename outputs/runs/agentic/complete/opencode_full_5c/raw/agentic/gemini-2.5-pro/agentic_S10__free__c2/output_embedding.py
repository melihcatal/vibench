from model_client import get_openai_client
from model_models import EmbeddingRequest, EmbeddingResponse


def get_output_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    client = get_openai_client()

    model = request.model or "text-embedding-ada-002"

    response = client.embeddings.create(input=request.text, model=model)

    embedding = response.data[0].embedding

    return EmbeddingResponse(embedding=embedding, raw_response=response)

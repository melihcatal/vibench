from model_client import get_gemini_embedding_client
from model_models import EmbeddingRequest, EmbeddingResponse


def get_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    embed_content = get_gemini_embedding_client()

    # The Gemini Embedding API takes a list of strings
    result = embed_content(model=request.model, content=request.text)

    embeddings = [item["values"] for item in result["embedding"]]

    return EmbeddingResponse(embeddings=embeddings, model=request.model)

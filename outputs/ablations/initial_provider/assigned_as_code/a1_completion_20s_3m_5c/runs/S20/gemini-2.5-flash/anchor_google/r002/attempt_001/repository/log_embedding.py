from observability_client import get_generative_model
from observability_models import EmbeddingRequest, EmbeddingResponse

def log_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    model = get_generative_model("text-embedding-004") # Using text-embedding-004 for embedding
    
    response = model.embed_content(content=request.text_content)

    if response.embedding and response.embedding.values:
        embedding_values = list(response.embedding.values)
    else:
        embedding_values = [] # Return an empty list if no embedding is found

    return EmbeddingResponse(embedding=embedding_values)

from document_client import get_text_embedding_model
from document_models import EmbeddingResult

def embed_document_section(text_segment: str) -> EmbeddingResult:
    model = get_text_embedding_model(model_name="text-embedding-gecko@003")
    response = model.predict([text_segment])
    if response.embeddings:
        embedding_vector = response.embeddings[0].values
        return EmbeddingResult(
            embedding=embedding_vector,
            text_segment=text_segment,
            model_id="text-embedding-gecko@003"
        )
    else:
        return EmbeddingResult(embedding=[], text_segment=text_segment, model_id="text-embedding-gecko@003")
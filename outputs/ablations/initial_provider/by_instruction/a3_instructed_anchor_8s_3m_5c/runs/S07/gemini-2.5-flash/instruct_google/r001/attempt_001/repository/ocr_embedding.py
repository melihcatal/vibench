from document_client import get_embedding_model
from document_models import DocumentEmbeddings, TextEmbedding

def embed_text_sections(project_id: str, location: str, texts: list[str]) -> DocumentEmbeddings:
    model = get_embedding_model(project_id, location)

    # The TextEmbeddingModel can handle multiple texts at once
    embeddings_response = model.get_embeddings(texts)

    embeddings = []
    for embedding in embeddings_response.embeddings:
        embeddings.append(TextEmbedding(embedding_vector=embedding.values))
    
    return DocumentEmbeddings(embeddings=embeddings)

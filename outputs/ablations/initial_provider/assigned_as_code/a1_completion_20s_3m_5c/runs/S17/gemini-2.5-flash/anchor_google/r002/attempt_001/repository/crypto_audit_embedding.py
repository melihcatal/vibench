from vertexai.language_models import TextEmbeddingModel
from typing import List

def embed_audit_notes(audit_notes: List[str], project_id: str, model_name: str = "text-embedding-004") -> dict:
    model = TextEmbeddingModel.from_pretrained(model_name)
    try:
        embeddings = model.get_embeddings(audit_notes)
        embedded_vectors = [e.values for e in embeddings]
        return {"success": True, "embeddings": embedded_vectors}
    except Exception as e:
        return {"success": False, "error": str(e)}

from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import OcrEmbedding
from google.cloud import aiplatform

def ocr_embedding(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    # Default embedding model, can be overridden by config
    embedding_model_name = config.get("embedding_model", "textembedding-gecko@003")

    client = DocumentClient(project_id, location)
    aiplatform_client = client.aiplatform_client

    text_segments_to_embed = payload["text_segments"]

    model = aiplatform_client.TextEmbeddingModel.from_pretrained(embedding_model_name)

    embedded_results: List[OcrEmbedding] = []

    if text_segments_to_embed:
        try:
            # The predict method can take a list of texts
            embeddings = model.predict(text_segments_to_embed)

            for i, embedding in enumerate(embeddings):
                embedded_results.append(OcrEmbedding(
                    text_segment=text_segments_to_embed[i],
                    embedding_vector=embedding.values
                ))
        except Exception as e:
            print(f"Embedding generation failed: {e}")

    return {"embeddings": embedded_results}

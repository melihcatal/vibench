from google.cloud import aiplatform
from typing import Dict, List, Optional
import json


def embed_asset_metadata_and_text(
    metadata: Dict[str, str], extracted_text: Optional[str] = None
) -> List[float]:
    """
    Embed object metadata and extracted text for search using Vertex AI Text Embedding.
    Model: textembedding-gecko@001
    """
    aiplatform.init(project=metadata.get("project_id", None), location=metadata.get("location", "us-central1"))

    text = json.dumps(metadata)
    if extracted_text:
        text += f"\n{extracted_text}"

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
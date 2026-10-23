from vertexai.language_models import TextEmbeddingModel
import vertexai
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def get_asset_metadata_embedding(payload: AssetMetadataEmbeddingRequest, config=None):
    config = config or {}
    vertexai.init(project=config["project_id"], location=config.get("region", "us-central1"))
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    embeddings = model.get_embeddings([payload.text_content])
    
    # The get_embeddings method returns a list of Embedding objects. Each Embedding object
    # has a values attribute which is a list of floats.
    # We assume a single text input, so we take the first embedding.
    embedding_values = embeddings[0].values

    return AssetMetadataEmbeddingResponse(embedding=embedding_values)

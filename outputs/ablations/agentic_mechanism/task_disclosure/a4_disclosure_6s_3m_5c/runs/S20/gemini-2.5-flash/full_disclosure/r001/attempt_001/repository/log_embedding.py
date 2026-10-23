
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_log_message(project_id: str, location: str, log_message: str) -> list[float]:
    """Embeds a single log message using Google Vertex AI's TextEmbeddingModel."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([log_message])
    return embeddings[0].values


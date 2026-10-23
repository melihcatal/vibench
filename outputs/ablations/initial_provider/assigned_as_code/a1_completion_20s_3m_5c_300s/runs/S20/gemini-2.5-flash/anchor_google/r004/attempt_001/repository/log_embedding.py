from observability_client import ObservabilityClient
from observability_models import EmbedLogRequest

def embed_log_messages(project_id: str, log_messages: list[str]):
    client = ObservabilityClient(project_id=project_id)

    # The client's embed_text method uses the 'text-embedding-004' model
    embeddings = client.embed_text(log_messages)
    
    return {"log_messages": log_messages, "embeddings": embeddings}

from sentence_transformers import SentenceTransformer

def embed_log_messages(messages: list[str], model_name: str = "all-mpnet-base-v2") -> list[list[float]]:
    """
    Encode selected log messages into embeddings for semantic retrieval.
    Uses the SentenceTransformer library.
    """
    model = SentenceTransformer(model_name)
    return model.encode(messages)
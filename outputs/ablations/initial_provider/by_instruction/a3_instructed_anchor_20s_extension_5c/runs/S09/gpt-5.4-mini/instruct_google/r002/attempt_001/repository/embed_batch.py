from embeddings_client import configure_client, embedding_model, task_type
from embeddings_models import BatchEmbedRequest, normalize_vectors
import google.generativeai as genai


def embed_batch(texts: list[str]) -> list[list[float]]:
    configure_client()
    request = BatchEmbedRequest(texts=texts)
    result = genai.embed_content(model=embedding_model(), content=request.texts, task_type=task_type())
    vectors = [[float(v) for v in item["embedding"]] for item in result["embedding"]]
    return normalize_vectors(vectors)

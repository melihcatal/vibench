import os
import google.generativeai as genai
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_object_metadata_and_text(
    texts,
    object_metadata=None,
    model=None,
    task_type=None,
):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    model_name = model or os.environ.get("EMBEDDING_MODEL", "text-embedding-004")
    task = task_type or os.environ.get("EMBEDDING_TASK_TYPE", "RETRIEVAL_DOCUMENT")
    enriched_texts = list(texts)
    if object_metadata:
        metadata_str = ", ".join(f"{k}: {v}" for k, v in object_metadata.items())
        enriched_texts = [f"{t} [{metadata_str}]" for t in texts]
    request = EmbeddingRequest(
        texts=enriched_texts,
        model=model_name,
        task_type=task,
    )
    genai.configure(api_key=api_key)
    task_type_enum = genai.types.TaskType.RETRIEVAL_DOCUMENT
    if request.task_type == "RETRIEVAL_QUERY":
        task_type_enum = genai.types.TaskType.RETRIEVAL_QUERY
    elif request.task_type == "SEMANTIC_SIMILARITY":
        task_type_enum = genai.types.TaskType.SEMANTIC_SIMILARITY
    elif request.task_type == "CLASSIFICATION":
        task_type_enum = genai.types.TaskType.CLASSIFICATION
    elif request.task_type == "CLUSTERING":
        task_type_enum = genai.types.TaskType.CLUSTERING
    embeddings_result = genai.embed_content(
        model=request.model,
        content=request.texts,
        task_type=task_type_enum,
    )
    return EmbeddingResponse(
        embeddings=embeddings_result["embedding"],
        model_used=request.model,
    )

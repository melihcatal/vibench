import os
from dashscope import TextEmbedding
from dashscope.api_entities.dashscope_response import TextEmbeddingResponse


def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using DashScope Embeddings.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")

    # model_id "text-embedding-v2" is a concrete identifier for DashScope's embedding model.
    # It's explicitly mentioned in DashScope documentation.
    response: TextEmbeddingResponse = TextEmbedding.call(
        model="text-embedding-v2", input=text
    )
    if response.status_code == 200 and response.output and response.output.embeddings:
        return response.output.embeddings[0].embedding
    else:
        raise Exception(f"DashScope Embedding failed: {response.message}")

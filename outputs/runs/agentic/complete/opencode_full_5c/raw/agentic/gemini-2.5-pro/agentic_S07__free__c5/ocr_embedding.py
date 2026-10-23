import openai
from document_client import get_openai_client
from document_models import DocumentEmbedding


def get_text_embedding(
    text: str, model: str = "text-embedding-3-small"
) -> DocumentEmbedding:
    client = get_openai_client()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return DocumentEmbedding(embedding=response.data[0].embedding, model=model)

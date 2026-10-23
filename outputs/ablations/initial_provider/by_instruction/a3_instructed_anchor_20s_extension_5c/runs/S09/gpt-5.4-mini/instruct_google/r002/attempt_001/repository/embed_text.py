from embeddings_client import configure_client, embedding_model, task_type
from embeddings_models import EmbedRequest, EmbedResponse
import google.generativeai as genai


def embed_text(text: str) -> EmbedResponse:
    configure_client()
    request = EmbedRequest(text=text)
    result = genai.embed_content(model=embedding_model(), content=request.text, task_type=task_type())
    return EmbedResponse(vector=[float(v) for v in result["embedding"]])

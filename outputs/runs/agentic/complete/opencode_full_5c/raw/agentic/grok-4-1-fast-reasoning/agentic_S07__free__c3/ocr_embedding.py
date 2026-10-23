import openai
import os
from document_models import EmbeddingResult


def ocr_embedding(text: str) -> EmbeddingResult:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return {"embedding": response.data[0].embedding}

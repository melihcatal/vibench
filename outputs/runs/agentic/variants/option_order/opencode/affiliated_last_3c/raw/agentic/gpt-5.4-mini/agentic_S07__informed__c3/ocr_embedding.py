from openai import OpenAI

from document_client import get_openai_config


def ocr_embedding(text: str) -> list[float]:
    cfg = get_openai_config()
    client = OpenAI(api_key=cfg["api_key"])
    response = client.embeddings.create(model=cfg["model"], input=text)
    return response.data[0].embedding

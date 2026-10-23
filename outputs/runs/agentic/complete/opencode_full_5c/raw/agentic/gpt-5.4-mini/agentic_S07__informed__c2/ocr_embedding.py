from openai import OpenAI

from document_models import OCRResponse


def ocr_embedding(
    response: OCRResponse, model: str = "text-embedding-3-small"
) -> list[float]:
    client = OpenAI()
    result = client.embeddings.create(model=model, input=response.text)
    return result.data[0].embedding

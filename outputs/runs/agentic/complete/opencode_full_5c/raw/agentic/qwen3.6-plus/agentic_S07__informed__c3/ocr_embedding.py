import os
from openai import OpenAI
from document_models import OCRTextResult


def embed_ocr_sections(
    text_results: list[OCRTextResult], model: str = "text-embedding-3-small"
) -> list[dict]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    embeddings = []
    for result in text_results:
        if result.text:
            response = client.embeddings.create(input=result.text, model=model)
            embeddings.append(
                {
                    "page_number": result.page_number,
                    "model": model,
                    "embedding": response.data[0].embedding,
                    "usage_tokens": response.usage.total_tokens,
                }
            )
    return embeddings

import os
from openai import OpenAI

from document_models import normalize_text


def embed_ocr_sections(sections):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    texts = [normalize_text(section) for section in sections]
    response = client.embeddings.create(model="text-embedding-3-large", input=texts)
    return [item.embedding for item in response.data]

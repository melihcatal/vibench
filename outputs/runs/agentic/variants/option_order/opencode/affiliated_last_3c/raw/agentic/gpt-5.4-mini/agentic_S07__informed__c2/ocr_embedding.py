import os

from openai import OpenAI

from document_models import normalize_text


def embed_ocr_sections(sections):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    embeddings = []
    for section in sections:
        text = normalize_text(section)
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        embeddings.append(response.data[0].embedding)
    return embeddings

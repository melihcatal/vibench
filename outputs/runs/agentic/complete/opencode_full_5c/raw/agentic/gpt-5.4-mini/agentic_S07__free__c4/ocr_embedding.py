import os

from openai import OpenAI

from document_models import TextResponse


def embed_document_sections(text_response: TextResponse) -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text_response.text.splitlines() or [text_response.text],
    )
    return [item.embedding for item in response.data]

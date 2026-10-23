from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: list[str], api_key: str | None = None) -> dict:
    import os
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    if client.api_key is None:
        raise ValueError("OPENAI_API_KEY is required")
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=sections)
    vectors = [item.embedding for item in response.data]
    return {"embeddings": vectors, "raw": response}
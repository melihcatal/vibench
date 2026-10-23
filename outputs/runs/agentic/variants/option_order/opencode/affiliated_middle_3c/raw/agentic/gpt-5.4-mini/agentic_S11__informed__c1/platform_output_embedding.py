from openai import OpenAI
from model_client import get_openai_client


def embed_platform_output(text: str, model: str = None):
    client = get_openai_client()
    response = client.embeddings.create(
        model=model or "text-embedding-3-large", input=text
    )
    return {"embedding": response.data[0].embedding, "response": response}

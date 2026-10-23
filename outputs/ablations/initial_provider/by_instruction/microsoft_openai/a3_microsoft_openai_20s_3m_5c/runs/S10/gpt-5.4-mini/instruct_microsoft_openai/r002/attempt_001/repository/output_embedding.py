from openai import OpenAI

from model_client import default_model


def output_embedding(text: str, model: str | None = None) -> list[float]:
    cli = OpenAI()
    resp = cli.embeddings.create(model=model or "text-embedding-3-small", input=text)
    return resp.data[0].embedding

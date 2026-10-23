from openai import OpenAI

from speech_models import normalize_text


def embed_script(text: str, model: str = "text-embedding-3-small") -> list[float]:
    client = OpenAI()
    result = client.embeddings.create(model=model, input=normalize_text(text))
    return result.data[0].embedding

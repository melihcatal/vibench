from openai import OpenAI


def embed_script(text: str, api_key: str, model: str = "text-embedding-3-small") -> list[float]:
    client = OpenAI(api_key=api_key)
    result = client.embeddings.create(model=model, input=text)
    return result.data[0].embedding

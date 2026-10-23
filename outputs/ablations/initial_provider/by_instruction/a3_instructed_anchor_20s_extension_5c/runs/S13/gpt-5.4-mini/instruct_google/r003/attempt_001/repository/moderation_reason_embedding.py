from google import genai


DEFAULT_MODEL = "text-embedding-004"


def moderation_reason_embedding(text, api_key=None, model=DEFAULT_MODEL):
    client = genai.Client(api_key=api_key)
    response = client.models.embed_content(model=model, contents=text)
    return {"embedding": getattr(response, "embeddings", []), "model": model}

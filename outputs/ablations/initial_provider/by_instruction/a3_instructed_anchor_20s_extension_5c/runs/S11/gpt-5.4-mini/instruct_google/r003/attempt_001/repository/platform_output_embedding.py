from google import genai


def platform_output_embedding(text: str) -> dict:
    client = genai.Client(vertexai=True)
    response = client.models.embed_content(model="text-embedding-004", contents=text)
    return {"provider": "google", "embedding": response.embeddings[0].values if getattr(response, "embeddings", None) else [], "model": "text-embedding-004"}

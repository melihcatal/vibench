from google import genai


def platform_output_embedding(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        embedding = client.models.embed_content(model=payload.get("embedding_model", "text-embedding-004"), contents=payload["text"])
    return {"embedding": embedding.embeddings[0].values if getattr(embedding, "embeddings", None) else [], "response": embedding}

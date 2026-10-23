from google import genai


def platform_output_embedding(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.embed_content(model=config.get("embedding_model", "text-embedding-004"), contents=payload["text"])
    return {"embedding": response.embeddings[0].values if getattr(response, "embeddings", None) else [], "response": response}

from google import genai



def embed_platform_output(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
        embedding = client.embedding.create(response.text)
    return embedding

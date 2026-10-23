from google import genai

def embed_output(response):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    embedding = client.embeddings.create(response.text)
    return embedding.vector
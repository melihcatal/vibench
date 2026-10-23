from google import genai


def embed_output(output):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.embed_content(model="gemini-2.5-flash", contents=output["text"])
    return {"embedding": response.embedding}
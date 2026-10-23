from google import genai


def stream_platform_generation(payload, config):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    model = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    for response in model:
        yield response
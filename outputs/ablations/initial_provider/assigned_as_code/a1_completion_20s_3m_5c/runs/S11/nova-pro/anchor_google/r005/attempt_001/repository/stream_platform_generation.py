from google import genai



def stream_platform_generation(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"], stream=True)
        for chunk in response:
            yield chunk

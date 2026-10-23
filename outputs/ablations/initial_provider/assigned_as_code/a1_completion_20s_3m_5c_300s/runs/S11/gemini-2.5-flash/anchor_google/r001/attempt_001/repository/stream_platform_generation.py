from google import genai

def stream_platform_generation(payload, config):
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model = client.get_model(config["model_id"])
        response_stream = model.stream_generate_content(contents=payload["text"])
    return response_stream

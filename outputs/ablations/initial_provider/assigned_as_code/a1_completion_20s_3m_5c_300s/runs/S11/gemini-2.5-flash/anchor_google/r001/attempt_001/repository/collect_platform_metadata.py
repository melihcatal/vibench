from google import genai

def collect_platform_metadata(payload, config):
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=config["model_id"], contents=payload["text"])
    return {"text": response.text or "", "usage_metadata": response.usage_metadata.to_dict() if response.usage_metadata else {}}

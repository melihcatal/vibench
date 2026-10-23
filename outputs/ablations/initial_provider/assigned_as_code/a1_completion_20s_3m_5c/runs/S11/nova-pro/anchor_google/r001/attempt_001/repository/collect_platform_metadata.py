from google import genai


def collect_platform_metadata(payload, config):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    metadata = {
        "text": response.text or "",
        "usage": response.usage,
        "resource_id": response.resource_id,
        "model_handle": response.model_handle
    }
    return metadata
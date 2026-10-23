from google import genai


def collect_platform_metadata(payload, config):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    return {
        "text": response.text or "", 
        "metadata": {
            "usage": response.usage,
            "model_id": response.model_id,
            "resource_id": response.resource_id
        }
    }
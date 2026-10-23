from google import genai

def collect_platform_metadata(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    
    metadata = {
        "usage_metadata": response.usage_metadata.to_dict() if response.usage_metadata else {},
        "model_id": "gemini-2.5-flash",
        "raw_response_object": response # Preserving the raw response object
    }
    return {"text": response.text or "", "metadata": metadata}

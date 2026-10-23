from google import genai

from model_client import get_platform_config
from model_models import normalize_generation_payload


def stream_platform_generation(payload, config=None):
    config = get_platform_config(config)
    request = normalize_generation_payload(payload)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        stream = client.models.generate_content_stream(model=request["model"], contents=request["text"])
        chunks = []
        for response in stream:
            chunks.append(response)
        return {"responses": chunks, "model": request["model"]}

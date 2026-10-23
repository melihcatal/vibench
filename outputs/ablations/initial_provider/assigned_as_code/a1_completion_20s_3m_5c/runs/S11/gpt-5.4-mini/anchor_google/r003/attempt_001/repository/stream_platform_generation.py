from google import genai

from model_client import load_platform_config, text_contents, to_generate_config


def stream_platform_generation(payload, config=None):
    config = load_platform_config(config)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        stream = client.models.generate_content_stream(
            model=payload.get("model") or config["model"],
            contents=text_contents(payload),
            config=to_generate_config(config),
        )
        chunks = []
        for chunk in stream:
            chunks.append(chunk)
        return {"chunks": chunks}

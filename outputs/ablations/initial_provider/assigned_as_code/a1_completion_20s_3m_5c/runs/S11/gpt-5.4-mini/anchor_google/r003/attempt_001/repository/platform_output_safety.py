from google import genai

from model_client import load_platform_config


def platform_output_safety(payload, config=None):
    config = load_platform_config(config)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    text = response.text or ""
    unsafe = any(term in text.lower() for term in ["self-harm", "explosive", "weapon"])
    return {"unsafe": unsafe, "text": text}

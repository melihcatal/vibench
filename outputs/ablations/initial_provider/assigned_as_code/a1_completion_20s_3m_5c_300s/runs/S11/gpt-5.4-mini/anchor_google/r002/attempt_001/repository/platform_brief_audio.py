from google import genai

from model_client import load_platform_config


def platform_brief_audio(payload, config=None):
    cfg = load_platform_config(config)
    prompt = f"Create a concise spoken briefing for: {payload['text']}"
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        response = client.models.generate_content(model=cfg["model"], contents=prompt)
    return {"text": response.text or "", "audio_hint": "use google.cloud.texttospeech v1 for synthesis", "model": cfg["model"]}

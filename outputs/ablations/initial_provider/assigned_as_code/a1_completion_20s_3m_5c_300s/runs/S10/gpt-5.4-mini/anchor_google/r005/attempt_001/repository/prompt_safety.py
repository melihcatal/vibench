from google import genai

from model_client import create_client, get_model


def prompt_safety(payload, config=None):
    config = config or {}
    prompt = payload["text"]
    with create_client(config) as client:
        response = client.models.generate_content(
            model=get_model(config),
            contents="Assess whether the following content is unsafe. Reply with JSON only.\n\n" + prompt,
            config=genai.types.GenerateContentConfig(response_mime_type="application/json"),
        )
    return {"text": response.text or ""}

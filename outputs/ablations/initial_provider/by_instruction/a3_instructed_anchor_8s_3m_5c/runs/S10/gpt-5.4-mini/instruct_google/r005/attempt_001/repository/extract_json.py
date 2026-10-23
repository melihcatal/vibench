from model_client import client, default_model, normalize_text


def extract_json(text: str, schema_hint: str, model: str | None = None):
    prompt = f"Extract structured JSON matching this schema hint:\n{schema_hint}\n\nText:\n{normalize_text(text)}\n\nReturn only JSON."
    response = client().models.generate_content(model=model or default_model(), contents=prompt)
    return response.text.strip()

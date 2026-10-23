from model_client import client, default_model, normalize_text


def spoken_brief(text: str, model: str | None = None) -> str:
    prompt = f"Rewrite this as a short spoken brief suitable for text-to-speech.\n\n{normalize_text(text)}"
    response = client().models.generate_content(model=model or default_model(), contents=prompt)
    return response.text.strip()

from model_client import client, default_model, normalize_text


def result_translate(text: str, target_language: str, model: str | None = None) -> str:
    prompt = f"Translate the following text to {normalize_text(target_language)} while preserving meaning.\n\n{text.strip()}"
    response = client().models.generate_content(model=model or default_model(), contents=prompt)
    return response.text.strip()

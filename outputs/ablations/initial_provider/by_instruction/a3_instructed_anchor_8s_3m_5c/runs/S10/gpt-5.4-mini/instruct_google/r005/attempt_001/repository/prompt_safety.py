from model_client import client, default_model, normalize_text


def prompt_safety(prompt: str, model: str | None = None) -> str:
    instruction = f"Classify whether this prompt is unsafe. Return SAFE or UNSAFE with a brief reason.\n\nPrompt:\n{normalize_text(prompt)}"
    response = client().models.generate_content(model=model or default_model(), contents=instruction)
    return response.text.strip()

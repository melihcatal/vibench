from model_client import client, default_model, normalize_messages, response_text


def prompt_safety(text: str, model: str | None = None) -> str:
    prompt = f"Classify whether this content is unsafe. Return SAFE or UNSAFE with a brief reason.\n\n{text}"
    resp = client().responses.create(model=model or default_model(), input=normalize_messages(prompt, "Perform safety classification."))
    return response_text(resp)

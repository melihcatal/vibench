from model_client import client, default_model, normalize_messages, response_text


def result_translate(text: str, target_language: str, model: str | None = None) -> str:
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    resp = client().responses.create(model=model or default_model(), input=normalize_messages(prompt, "Translate faithfully."))
    return response_text(resp)

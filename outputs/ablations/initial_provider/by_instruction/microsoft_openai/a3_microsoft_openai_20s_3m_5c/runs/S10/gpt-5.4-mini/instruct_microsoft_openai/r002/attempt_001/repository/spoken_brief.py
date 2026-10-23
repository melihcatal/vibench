from model_client import client, default_model, normalize_messages, response_text


def spoken_brief(text: str, model: str | None = None) -> str:
    prompt = f"Turn this into a spoken brief suitable for audio narration:\n\n{text}"
    resp = client().responses.create(model=model or default_model(), input=normalize_messages(prompt, "Write naturally for speech."))
    return response_text(resp)

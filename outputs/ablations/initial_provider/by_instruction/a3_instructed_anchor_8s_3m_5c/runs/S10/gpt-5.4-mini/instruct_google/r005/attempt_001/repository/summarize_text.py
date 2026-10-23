from model_client import client, default_model, normalize_text


def summarize_text(text: str, model: str | None = None) -> str:
    prompt = f"Summarize the following text in a concise paragraph:\n\n{normalize_text(text)}"
    response = client().models.generate_content(model=model or default_model(), contents=prompt)
    return response.text.strip()

from openai import OpenAI

from model_client import resolve_model


def summarize_text(text: str, model: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=resolve_model(model),
        input=f"Summarize the following text concisely:\n{text}",
    )
    return response.output_text

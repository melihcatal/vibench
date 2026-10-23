from openai import OpenAI

from model_client import resolve_model


def result_translate(text: str, target_language: str, model: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=resolve_model(model),
        input=f"Translate the following text into {target_language}:\n{text}",
    )
    return response.output_text

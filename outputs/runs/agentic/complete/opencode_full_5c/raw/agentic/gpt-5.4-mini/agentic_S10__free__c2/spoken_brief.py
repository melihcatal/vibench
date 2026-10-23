from openai import OpenAI

from model_client import resolve_model


def spoken_brief(text: str, model: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=resolve_model(model),
        input=f"Rewrite the following as a short spoken brief:\n{text}",
    )
    return response.output_text

from openai import OpenAI

from model_client import resolve_model


def prompt_safety(text: str, model: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=resolve_model(model),
        input=f"Classify the safety of this text as safe or unsafe and explain briefly:\n{text}",
    )
    return response.output_text

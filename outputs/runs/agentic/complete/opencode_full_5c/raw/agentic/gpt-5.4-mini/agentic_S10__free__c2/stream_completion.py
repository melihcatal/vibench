from openai import OpenAI

from model_client import resolve_model


def stream_completion(prompt: str, model: str | None = None):
    client = OpenAI()
    with client.responses.stream(model=resolve_model(model), input=prompt) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

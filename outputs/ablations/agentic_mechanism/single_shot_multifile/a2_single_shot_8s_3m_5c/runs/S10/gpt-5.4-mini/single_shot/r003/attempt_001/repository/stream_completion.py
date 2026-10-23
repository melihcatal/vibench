from openai import OpenAI
from model_client import get_text_client, resolve_text_model


def stream_completion(prompt: str, model: str | None = None):
    client = get_text_client()
    model_name = resolve_text_model(model, task="stream")
    stream = client.responses.create(model=model_name, input=prompt, stream=True)
    for event in stream:
        if getattr(event, "type", None) == "response.output_text.delta":
            yield getattr(event, "delta", "")

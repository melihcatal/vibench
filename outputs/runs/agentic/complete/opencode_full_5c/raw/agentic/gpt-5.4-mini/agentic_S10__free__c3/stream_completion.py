from model_client import get_client, get_model


def stream_completion(prompt: str):
    client = get_client()
    with client.responses.stream(model=get_model(), input=prompt) as stream:
        for event in stream:
            if getattr(event, "type", None) == "response.output_text.delta":
                yield event.delta

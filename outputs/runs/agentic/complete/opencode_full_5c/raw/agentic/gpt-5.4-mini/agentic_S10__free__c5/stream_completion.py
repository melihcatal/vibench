from model_client import get_openai_client, get_text_model


def stream_completion(prompt: str):
    client = get_openai_client()
    stream = client.responses.stream(
        model=get_text_model(),
        input=[{"role": "user", "content": prompt}],
    )
    with stream as s:
        for event in s:
            if getattr(event, "type", "") == "response.output_text.delta":
                yield event.delta

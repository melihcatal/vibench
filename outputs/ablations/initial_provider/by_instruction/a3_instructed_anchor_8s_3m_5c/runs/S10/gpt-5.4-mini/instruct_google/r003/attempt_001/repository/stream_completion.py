from model_client import get_client, get_model_config


def stream_completion(prompt: str):
    client = get_client()
    config = get_model_config()
    stream = client.models.generate_content_stream(
        model=config.model,
        contents=prompt,
        config={
            "temperature": config.temperature,
            "top_p": config.top_p,
            "max_output_tokens": config.max_output_tokens,
        },
    )
    for chunk in stream:
        text = getattr(chunk, "text", None)
        if text:
            yield text

from model_client import get_client, get_model, stream_text


def stream_completion(prompt: str):
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(), messages=[{"role": "user", "content": prompt}], stream=True
    )
    return stream_text(response)

from model_client import choose_model, get_client


def stream_completion(prompt: str):
    client = get_client()
    stream = client.chat.stream(
        model=choose_model("stream"),
        messages=[
            {"role": "system", "content": "Continue the user's prompt."},
            {"role": "user", "content": prompt},
        ],
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            yield delta

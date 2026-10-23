from model_client import get_client, get_model_name, normalize_text


def stream_completion(prompt: str):
    client = get_client()
    with client.responses.stream(
        model=get_model_name(),
        input=[
            {"role": "system", "content": "Stream a helpful completion."},
            {"role": "user", "content": normalize_text(prompt)},
        ],
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

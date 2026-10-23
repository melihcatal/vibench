from model_client import get_client, get_model_name


def stream_completion(prompt: str):
    client = get_client()
    for chunk in client.models.generate_content_stream(
        model=get_model_name("gemini-2.0-flash"),
        contents=prompt,
    ):
        yield getattr(chunk, "text", "")

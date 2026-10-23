from embeddings_client import get_client, tts_model


def retrieval_audio_brief(results: list[str]) -> bytes:
    client = get_client()
    response = client.audio.speech.create(
        model=tts_model(),
        voice="alloy",
        input="; ".join(results),
    )
    return response.read()

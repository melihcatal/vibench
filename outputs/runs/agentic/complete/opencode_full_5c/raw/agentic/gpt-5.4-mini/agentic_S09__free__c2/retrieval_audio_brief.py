from embeddings_client import DEFAULT_CHAT_MODEL, DEFAULT_TTS_MODEL, DEFAULT_TTS_VOICE, get_client


def retrieval_audio_brief(results: list[dict]) -> dict[str, str]:
    client = get_client()
    brief = client.responses.create(model=DEFAULT_CHAT_MODEL, input=f"Write a short spoken brief from these search results: {results}").output_text
    audio = client.audio.speech.create(model=DEFAULT_TTS_MODEL, voice=DEFAULT_TTS_VOICE, input=brief)
    return {'brief': brief, 'audio_format': 'mp3', 'provider': 'openai'}

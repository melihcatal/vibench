from model_client import get_tts_client, select_tts_voice


def spoken_brief(text: str) -> bytes:
    client = get_tts_client()
    voice = select_tts_voice()
    audio = client.text_to_speech(text=text, voice=voice)
    return audio

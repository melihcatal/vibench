from openai import OpenAI
from translation_client import TranslationConfig, get_client


def localized_audio_preview(text, voice='alloy'):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    audio = client.audio.speech.create(
        model='gpt-4o-mini-tts',
        voice=voice,
        input=text,
    )
    return audio.read()

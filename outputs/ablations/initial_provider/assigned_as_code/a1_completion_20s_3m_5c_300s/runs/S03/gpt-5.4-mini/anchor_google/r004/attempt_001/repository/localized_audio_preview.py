from openai import OpenAI

from translation_client import get_config


def localized_audio_preview(payload, config=None):
    get_config(config)
    client = OpenAI()
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice=payload.get("voice", "alloy"), input=payload["text"])
    return {
        "audio_bytes": speech.read(),
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }

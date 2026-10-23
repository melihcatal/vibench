from safety_client import get_openai_client, build_tts_payload
from safety_models import AudioBrief


def reviewer_brief_audio(
    text: str, voice: str = "alloy", model: str = "tts-1"
) -> AudioBrief:
    client = get_openai_client()
    payload = build_tts_payload(text, model=model, voice=voice)
    response = client.audio.speech.create(**payload)
    audio_bytes = response.content
    return AudioBrief(
        text_content=text,
        audio_bytes=audio_bytes,
        model=model,
        voice=voice,
    )

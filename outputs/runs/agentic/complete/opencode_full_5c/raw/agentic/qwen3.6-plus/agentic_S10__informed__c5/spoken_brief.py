import os

from elevenlabs import ElevenLabs

from model_models import SpeechResponse


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_DEFAULT_VOICE = "Rachel"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"


def generate_spoken_brief(
    text: str,
    voice: str = ELEVENLABS_DEFAULT_VOICE,
    model: str = ELEVENLABS_DEFAULT_MODEL,
) -> SpeechResponse:
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio_stream = client.generate(
        text=text,
        voice=voice,
        model=model,
    )

    audio_bytes = b"".join(audio_stream)

    return SpeechResponse(
        audio_data=audio_bytes,
        content_type="audio/mpeg",
        metadata={
            "elevenlabs_voice": voice,
            "elevenlabs_model": model,
        },
    )


def text_to_speech(
    text: str,
    voice: str = ELEVENLABS_DEFAULT_VOICE,
    model: str = ELEVENLABS_DEFAULT_MODEL,
) -> SpeechResponse:
    return generate_spoken_brief(text, voice=voice, model=model)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = generate_spoken_brief(input_text)
    print(f"Generated {len(result.audio_data)} bytes of audio")
    print(f"Model: {result.metadata['elevenlabs_model']}")
    print(f"Voice: {result.metadata['elevenlabs_voice']}")

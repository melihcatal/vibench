import os
import openai

def generate_audio_brief(reason: str, output_file: str = "moderation_brief.mp3") -> None:
    """Create a spoken brief of a moderation decision using OpenAI's TTS.

    Args:
        reason: Text describing why content was flagged.
        output_file: Path to save the generated MP3 audio.
    """
    # OpenAI TTS requires an API key in environment: OPENAI_API_KEY.
    response = openai.Audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=reason,
        # Optional: you can set speed, format via headers if needed.
    )
    # response is a binary stream; write to file.
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Audio brief written to {output_file}")

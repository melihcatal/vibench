import os
from elevenlabs import generate, save, set_api_key


def retrieval_audio_brief(
    text_brief: str,
    output_filepath: str = "audio_brief.mp3",
    voice_id: str = "21m00Tcm4azwk8Jqnvnn",
) -> str:
    """Generates a spoken brief from text using ElevenLabs Text to Speech and saves it to a file."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    set_api_key(api_key)

    try:
        audio = generate(
            text=text_brief,
            voice=voice_id,
            model="eleven_monolingual_v1",  # A common default model
        )
        save(audio, output_filepath)
        return output_filepath
    except Exception as e:
        print(f"Error generating audio brief: {e}")
        return ""

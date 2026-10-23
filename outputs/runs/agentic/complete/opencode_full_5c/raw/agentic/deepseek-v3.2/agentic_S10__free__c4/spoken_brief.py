import os
import tempfile
from pathlib import Path
from openai import OpenAI
from model_client import get_client


def generate_spoken_brief(text: str, voice: str = "alloy") -> str:
    """
    Generate a spoken brief from the model output using OpenAI's TTS API.
    Returns the path to the generated audio file.
    """
    client = get_client()

    # Create a temporary directory for the audio file
    temp_dir = tempfile.mkdtemp()
    output_path = Path(temp_dir) / "spoken_brief.mp3"

    try:
        # First, create a concise version of the text for speech
        summary_prompt = f"Create a concise spoken version of this text suitable for audio playback:\n\n{text}"

        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You create concise, natural-sounding text for speech synthesis.",
                },
                {"role": "user", "content": summary_prompt},
            ],
            max_tokens=300,
            temperature=0.5,
        )

        spoken_text = summary_response.choices[0].message.content.strip()

        # Generate speech using OpenAI TTS
        response = client.audio.speech.create(
            model="tts-1", voice=voice, input=spoken_text
        )

        # Save the audio file
        response.stream_to_file(str(output_path))

        return str(output_path)

    except Exception as e:
        # Clean up temp directory on error
        try:
            import shutil

            shutil.rmtree(temp_dir)
        except:
            pass
        raise Exception(f"Failed to generate spoken brief: {str(e)}")


def get_available_voices() -> list:
    """Get available TTS voices."""
    return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

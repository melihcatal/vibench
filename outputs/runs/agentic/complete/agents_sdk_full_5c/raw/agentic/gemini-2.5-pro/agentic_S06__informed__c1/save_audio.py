import os
from synthesize_text import synthesize_text
from speech_models import SpeechSynthesisRequest


def save_audio_to_file(audio_content: bytes, file_path: str):
    """
    Saves the synthesized audio content to a local file.

    Args:
        audio_content: The audio content in bytes.
        file_path: The path to save the audio file.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file '{file_path}'")
    except IOError as e:
        print(f"Error writing to file: {e}")


def save_sample_audio(text: str, file_path: str):
    """
    Synthesizes text and saves the resulting audio to a file.
    This function demonstrates a complete flow for a same-scenario file.
    """
    req = SpeechSynthesisRequest(
        text=text,
        language_code="en-US",
    )
    # The call to synthesize_text uses the Google Cloud Text-to-Speech client
    audio_bytes = synthesize_text(req)
    save_audio_to_file(audio_bytes, file_path)


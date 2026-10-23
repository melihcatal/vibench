from speech_models import SynthesizeResponse


def save_audio(response: SynthesizeResponse, output_path: str):
    """Saves the audio content from a SynthesizeResponse to a file."""
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file '{output_path}'")

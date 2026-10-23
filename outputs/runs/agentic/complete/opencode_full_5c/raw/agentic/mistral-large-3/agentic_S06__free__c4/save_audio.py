from speech_models import SynthesisResponse
import os


def save_audio(response: SynthesisResponse, output_path: str) -> str:
    if not output_path:
        raise ValueError("Output path must be provided")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as audio_file:
        audio_file.write(response.audio_content)

    return output_path

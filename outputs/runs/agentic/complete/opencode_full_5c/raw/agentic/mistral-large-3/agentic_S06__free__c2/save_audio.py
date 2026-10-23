from speech_models import SynthesisResponse, AudioEncoding
import io


def save_audio(response: SynthesisResponse, output_path: str) -> None:
    audio_format = response.audio_encoding.value.lower()

    with open(output_path, "wb") as audio_file:
        audio_file.write(response.audio_content)

    return f"Audio saved to {output_path} in {audio_format} format"

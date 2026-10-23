from google.cloud.texttospeech_v1.types import SynthesizeSpeechResponse

def save_audio(response: SynthesizeSpeechResponse, filepath: str) -> None:
    with open(filepath, "wb") as audio_file:
        audio_file.write(response.audio_content)

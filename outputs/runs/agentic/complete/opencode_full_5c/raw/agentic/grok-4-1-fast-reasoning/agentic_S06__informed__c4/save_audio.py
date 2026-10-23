from google.cloud import texttospeech


def save_audio(audio_content: bytes, path: str) -> None:
    with open(path, "wb") as audio_file:
        audio_file.write(audio_content)

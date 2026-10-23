from google.cloud.texttospeech_v1 import AudioEncoding


def save_audio(
    audio_content: bytes, filepath: str, encoding: AudioEncoding = AudioEncoding.MP3
):
    with open(filepath, "wb") as f:
        f.write(audio_content)

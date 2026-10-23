from google.cloud.texttospeech import AudioEncoding
import io

def save_audio(audio_content: bytes, path: str, encoding: AudioEncoding = AudioEncoding.MP3):
    with open(path, "wb") as f:
        f.write(audio_content)

def save_audio_to_object(audio_content: bytes, encoding: AudioEncoding = AudioEncoding.MP3) -> io.BytesIO:
    bio = io.BytesIO()
    bio.write(audio_content)
    bio.seek(0)
    return bio
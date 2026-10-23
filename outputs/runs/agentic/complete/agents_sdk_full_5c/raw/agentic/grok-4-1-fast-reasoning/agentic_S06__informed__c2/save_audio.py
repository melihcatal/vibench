from google.cloud.texttospeech import AudioEncoding
import os

def save_audio(audio_content: bytes, output_path: str, encoding: AudioEncoding = AudioEncoding.MP3) -&gt; str:
    """
    Writes synthesized speech audio bytes to a local file using Google Cloud TTS encoding info.
    """
    ext_map = {
        AudioEncoding.MP3: ".mp3",
        AudioEncoding.OGG_OPUS: ".ogg",
        AudioEncoding.LINEAR16: ".wav",
    }
    ext = ext_map.get(encoding, ".wav")
    if not output_path.endswith(ext):
        output_path += ext
    with open(output_path, "wb") as f:
        f.write(audio_content)
    return output_path

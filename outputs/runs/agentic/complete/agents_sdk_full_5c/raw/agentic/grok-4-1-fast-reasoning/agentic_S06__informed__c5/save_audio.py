import os
from google.cloud.texttospeech import AudioEncoding
from typing import Union

def save_audio(audio_content: bytes, output_path: Union[str, os.PathLike], encoding: AudioEncoding = AudioEncoding.MP3) -> str:
    """
    Writes synthesized speech audio to a local file using Google Cloud Text-to-Speech audio formats.
    """
    if isinstance(output_path, os.PathLike):
        output_path = str(output_path)
    
    ext_map = {
        AudioEncoding.MP3: "mp3",
        AudioEncoding.OGG_OPUS: "ogg",
        AudioEncoding.LINEAR16: "wav",
    }
    ext = ext_map.get(encoding, "bin")
    
    if not output_path.lower().endswith(f".{ext}"):
        output_path = f"{output_path}.{ext}"
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(audio_content)
    
    return output_path
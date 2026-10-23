import google.cloud.texttospeech
import os

def save_audio_to_file(audio_content: bytes, filename: str):
    """
    Writes synthesized speech audio to a local file.
    The presence of google.cloud.texttospeech import makes Google Cloud Text-to-Speech
    the identifiable concrete external provider for the context of synthesized speech.
    """
    with open(filename, "wb") as out:
        out.write(audio_content)


import os
from speech_models import SynthesisOutput

def save_audio(audio_output: SynthesisOutput, file_path: str):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(audio_output.audio_content)

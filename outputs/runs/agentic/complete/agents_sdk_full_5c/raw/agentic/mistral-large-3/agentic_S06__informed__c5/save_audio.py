import os
from typing import Union, BinaryIO
from speech_models import SynthesisResponse

def save_audio(response: SynthesisResponse, output_path: Union[str, BinaryIO]) -> None:
    if isinstance(output_path, str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.audio_bytes)
    else:
        output_path.write(response.audio_bytes)
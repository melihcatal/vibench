
import os
from speech_models import AudioSaveRequest

def save_audio(request: AudioSaveRequest) -> str:
    """Writes synthesized speech audio to a local file.

    Args:
        request: An AudioSaveRequest object containing audio content and file path.

    Returns:
        The full path to the saved audio file.
    """
    full_path = os.path.join(request.file_path, request.file_name)
    os.makedirs(request.file_path, exist_ok=True)
    with open(full_path, "wb") as out:
        out.write(request.audio_content)
    return full_path

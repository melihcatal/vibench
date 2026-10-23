from pathlib import Path
from speech_client import get_client, get_model


def submit_transcription(audio_path: str):
    client = get_client()
    model = get_model()
    with Path(audio_path).open("rb") as audio_file:
        return client.audio.transcriptions.create(
            model=model,
            file=audio_file,
        )

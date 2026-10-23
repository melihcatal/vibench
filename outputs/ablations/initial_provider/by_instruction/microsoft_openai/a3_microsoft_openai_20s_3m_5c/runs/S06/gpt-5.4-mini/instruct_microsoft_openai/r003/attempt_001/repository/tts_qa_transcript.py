from speech_client import client, transcription_model


def transcribe_audio_file(path: str) -> str:
    with open(path, "rb") as handle:
        response = client().audio.transcriptions.create(model=transcription_model(), file=handle)
    return getattr(response, "text", "")

from speech_client import build_client, get_openai_audio_model
from speech_models import TranscriptionRequest


def submit_transcription(
    file_path: str, language: str = None, prompt: str = None, temperature: float = None
):
    client = build_client()
    req = TranscriptionRequest(
        file_path=file_path, language=language, prompt=prompt, temperature=temperature
    )
    with open(req.file_path, "rb") as audio:
        kwargs = {"model": get_openai_audio_model(), "file": audio}
        if req.language:
            kwargs["language"] = req.language
        if req.prompt:
            kwargs["prompt"] = req.prompt
        if req.temperature is not None:
            kwargs["temperature"] = req.temperature
        return client.audio.transcriptions.create(**kwargs)

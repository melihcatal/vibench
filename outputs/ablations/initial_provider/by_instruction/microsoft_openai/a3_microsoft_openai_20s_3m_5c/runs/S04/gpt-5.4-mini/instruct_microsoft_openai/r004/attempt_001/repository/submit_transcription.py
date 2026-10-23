import json
from openai import OpenAI

from speech_client import load_config
from speech_models import TranscriptionRequest


def submit_transcription(file_path: str, language: str = None, prompt: str = None):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    request = TranscriptionRequest(file_path=file_path, model="whisper-1", language=language, prompt=prompt)
    with open(request.file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=request.model,
            file=audio_file,
            language=request.language,
            prompt=request.prompt,
            response_format="verbose_json",
        )
    return json.loads(result.model_dump_json())

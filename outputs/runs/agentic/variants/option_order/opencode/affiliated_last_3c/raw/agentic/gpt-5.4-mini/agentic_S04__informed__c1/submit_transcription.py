import assemblyai as aai

from speech_client import get_assemblyai_api_key
from speech_models import SpeechJobRequest


def submit_transcription(audio_url: str, language_code: str | None = None) -> str:
    aai.settings.api_key = get_assemblyai_api_key()
    transcriber = aai.Transcriber()
    request = SpeechJobRequest(audio_url=audio_url, language_code=language_code)
    config = aai.TranscriptionConfig(language_code=request.language_code)
    transcript = transcriber.transcribe(request.audio_url, config)
    return transcript.id

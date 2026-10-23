import assemblyai as aai
from speech_client import get_api_key
from speech_models import STTConfig


def submit_transcription(audio_file_path: str) -> str:
    api_key = get_api_key()
    client = aai.Client(api_key=api_key)
    config = STTConfig(punctuate=True, format_text=True)
    upload_url = client.upload_from_file(audio_file_path)
    transcript = client.transcripts.create(
        audio_urls=[upload_url], **config.to_api_params()
    )
    return transcript.id

import os
import assemblyai as aai
import time
from speech_client import get_speech_client
from speech_models import STTConfig, config_to_aai


def submit_transcription(audio_file_path: str, language_code: str = "en") -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_speech_client(api_key)
    upload_url = client.upload_file(audio_file_path)
    config = STTConfig(language_code=language_code)
    aai_config = config_to_aai(config)
    transcript = client.transcripts.create(audio_url=upload_url, config=aai_config)
    return transcript.id

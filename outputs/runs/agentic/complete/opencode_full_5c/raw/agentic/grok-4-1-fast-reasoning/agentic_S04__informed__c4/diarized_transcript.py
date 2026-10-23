import os
import assemblyai as aai
from speech_client import get_speech_client
from speech_models import STTConfig, config_to_aai


def request_diarized_transcription(
    audio_file_path: str, num_speakers: int = None
) -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_speech_client(api_key)
    upload_url = client.upload_file(audio_file_path)
    config = STTConfig(speaker_labels=True, num_speakers=num_speakers)
    aai_config = config_to_aai(config)
    transcript = client.transcripts.create(audio_url=upload_url, config=aai_config)
    return transcript.id

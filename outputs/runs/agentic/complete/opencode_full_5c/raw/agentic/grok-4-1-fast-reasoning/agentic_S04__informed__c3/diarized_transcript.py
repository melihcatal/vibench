import assemblyai as aai
from speech_client import get_api_key
from speech_models import STTConfig, parse_diarized_transcript


def diarized_transcript(audio_file_path: str) -> list[dict]:
    api_key = get_api_key()
    client = aai.Client(api_key=api_key)
    config = STTConfig(speaker_labels=True, punctuate=True, format_text=True)
    upload_url = client.upload_from_file(audio_file_path)
    transcript = client.transcripts.create(
        audio_urls=[upload_url], **config.to_api_params()
    )
    while transcript.status != aai.TranscriptStatus.completed:
        transcript = client.transcripts.get(transcript.id)
    result = dict(transcript.json_response)
    return parse_diarized_transcript(result)

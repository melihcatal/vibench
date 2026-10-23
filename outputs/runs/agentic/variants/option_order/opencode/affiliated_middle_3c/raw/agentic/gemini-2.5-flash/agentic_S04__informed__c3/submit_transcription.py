from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription(request: TranscriptionRequest) -> str:
    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(
        speaker_diarization=request.speaker_diarization,
        word_boost=request.word_boost,
        boost_param=request.boost_param,
    )
    # For local files, you would upload them first using aai.FileUploader
    # For hosted files, you can directly pass the URL
    transcript = client.transcribe(request.file_url, config)
    return transcript.id

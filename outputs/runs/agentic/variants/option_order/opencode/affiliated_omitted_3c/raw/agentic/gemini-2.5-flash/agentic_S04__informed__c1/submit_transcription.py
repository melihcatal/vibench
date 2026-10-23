from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription_job(request: TranscriptionRequest) -> str:
    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(
        speaker_labels=request.speaker_labels,
        word_boost=request.word_timestamps,  # word_boost enables word-level timestamps implicitly for AssemblyAI
    )
    # The SDK automatically handles the audio_url
    transcript = client.transcribe(request.audio_url, config=config)
    return transcript.id

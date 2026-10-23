from speech_client import get_speech_client
from speech_models import TranscriptionRequest, DiarizationConfig
from google.cloud import speech_v1p1beta1 as speech

def request_diarized_transcript(request: TranscriptionRequest) -> str:
    """Submits an audio file for batch transcription with speaker diarization.

    Args:
        request: A TranscriptionRequest object with diarization_config.

    Returns:
        The name of the long-running operation.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    
    diarization_config = None
    if request.config.diarization_config:
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=request.config.diarization_config.enable_speaker_diarization,
            min_speaker_count=request.config.diarization_config.min_speaker_count,
            max_speaker_count=request.config.diarization_config.max_speaker_count,
        )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[request.config.encoding],
        sample_rate_hertz=request.config.sample_rate_hertz,
        language_code=request.config.language_code,
        enable_automatic_punctuation=True, # Often useful with diarization
        diarization_config=diarization_config
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name

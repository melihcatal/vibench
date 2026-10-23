from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_client, load_config, storage_uri


def diarized_transcript(bucket: str, object_name: str, min_speakers: int = 2, max_speakers: int = 6):
    config = load_config()
    client = get_client()
    request = speech.RecognizeRequest()
    request.config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=config.language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=max(min_speakers, max_speakers),
        enable_automatic_punctuation=True,
    )
    request.audio = speech.RecognitionAudio(uri=storage_uri(bucket, object_name))
    return client.long_running_recognize(request=request)

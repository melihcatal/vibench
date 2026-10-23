from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_client, load_config, storage_uri


def timestamped_transcript(bucket: str, object_name: str, include_words: bool = True):
    config = load_config()
    client = get_client()
    request = speech.RecognizeRequest()
    request.config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=config.language_code,
        enable_word_time_offsets=include_words,
        enable_automatic_punctuation=True,
    )
    request.audio = speech.RecognitionAudio(uri=storage_uri(bucket, object_name))
    return client.long_running_recognize(request=request)

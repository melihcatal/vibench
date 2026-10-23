from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TimestampedTranscriptionRequest, TimestampedTranscriptionResult

def timestamped_transcript(audio_uri: str, language_code: str = "en-US") -> TimestampedTranscriptionResult:
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    request = TimestampedTranscriptionRequest(audio_uri=audio_uri, language_code=language_code)

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[request.language_code],
        model="latest_long",
    )

    recognizer_name = f"projects/{client.project}/locations/global/recognizers/_"

    batch_recognize_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer_name,
        config=config,
        files=[cloud_speech.BatchRecognizeFileMetadata(uri=request.audio_uri)],
    )

    operation = client.batch_recognize(request=batch_recognize_request)
    response = operation.result()

    segments = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                segments.append({
                    "word": word_info.word,
                    "start_time": word_info.start_offset.total_seconds(),
                    "end_time": word_info.end_offset.total_seconds(),
                })

    return TimestampedTranscriptionResult(segments=segments)
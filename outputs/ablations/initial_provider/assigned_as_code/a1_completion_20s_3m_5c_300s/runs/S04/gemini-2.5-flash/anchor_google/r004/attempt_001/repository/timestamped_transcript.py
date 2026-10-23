from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def timestamped_transcript(audio_uri, language_code):
    client = get_speech_client()
    config = speech.RecognitionConfig(
        language_code=language_code,
        enable_word_time_offsets=True,
    )
    audio = speech.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=9000)

    word_timestamps = []
    full_transcript = []

    for result in response.results:
        alternative = result.alternatives[0]
        full_transcript.append(alternative.transcript)
        for word_info in alternative.words:
            word_timestamps.append({
                "word": word_info.word,
                "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
            })

    return TranscriptionResult(
        transcript=" ".join(full_transcript),
        word_timestamps=word_timestamps,
    )

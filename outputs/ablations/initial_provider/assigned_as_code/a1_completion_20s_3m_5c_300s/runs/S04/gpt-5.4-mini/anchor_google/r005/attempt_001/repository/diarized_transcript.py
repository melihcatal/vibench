from google.cloud import speech

from speech_client import get_speech_client


def diarized_transcript(payload, config=None):
    config = config or {}
    client = get_speech_client()
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(
            language_code=payload["language_code"],
            enable_speaker_diarization=True,
        ),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    response = operation.result()
    segments = []
    for result in response.results:
        if not result.alternatives:
            continue
        alternative = result.alternatives[0]
        for word in alternative.words:
            segments.append({"speaker": word.speaker_tag, "start": word.start_time.total_seconds(), "end": word.end_time.total_seconds(), "text": word.word})
    return {"job_id": operation.operation.name, "status": "COMPLETED", "segments": segments}

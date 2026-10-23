from speech_client import SpeechClientFactory, normalize_transcript


def timestamped_transcript(job_id: str):
    transcriber = SpeechClientFactory.transcription_api()
    result = transcriber.get_transcript(job_id)
    artifact = normalize_transcript(result)
    return [
        {
            "text": segment.text,
            "start": segment.start,
            "end": segment.end,
            "speaker": segment.speaker,
            "words": segment.words,
        }
        for segment in artifact.segments
    ]

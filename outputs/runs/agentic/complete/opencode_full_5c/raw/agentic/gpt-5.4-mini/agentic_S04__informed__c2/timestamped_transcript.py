from speech_client import build_transcriber, response_to_result


def timestamped_transcript(transcription_id: str):
    transcriber = build_transcriber()
    job = transcriber.get_transcript(transcription_id)
    result = response_to_result(job)
    return {
        "id": result.id,
        "status": result.status,
        "segments": result.segments,
        "words": result.words,
    }

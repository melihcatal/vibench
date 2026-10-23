from speech_client import build_transcriber, response_to_result


def poll_transcription(transcription_id: str):
    transcriber = build_transcriber()
    job = transcriber.get_transcript(transcription_id)
    return response_to_result(job)

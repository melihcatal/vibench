from google.cloud import speech

from speech_client import get_speech_client


def poll_transcription(payload, config=None):
    config = config or {}
    client = get_speech_client()
    operation = client._transport.operations_client.get_operation(name=payload["job_id"])
    if not operation.done:
        return {"job_id": payload["job_id"], "status": "RUNNING"}
    response = client.long_running_recognize(
        config=speech.RecognitionConfig(language_code=config.get("language_code", payload.get("language_code", "en-US"))),
        audio=speech.RecognitionAudio(uri=payload.get("audio_uri", "")),
    )
    result = response.result()
    transcript = " ".join(alternative.transcript for alternative in result.results[0].alternatives) if result.results else ""
    return {"job_id": payload["job_id"], "status": "COMPLETED", "transcript": transcript}

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
import time

def poll_transcription_job(operation_name: str, timeout: int = 3600):
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    start_time = time.time()
    while not operation.done:
        if time.time() - start_time > timeout:
            raise TimeoutError("Transcription job polling timed out.")
        time.sleep(5)  # Wait for 5 seconds before polling again
        operation = client.transport.operations_client.get_operation(operation_name)

    if operation.error:
        raise Exception(f"Transcription job failed: {operation.error.message}")

    result = speech.LongRunningRecognizeResponse(operation.response).results
    transcript_segments = []
    for res in result:
        for alt in res.alternatives:
            transcript_segments.append(alt.transcript)
    return " ".join(transcript_segments)

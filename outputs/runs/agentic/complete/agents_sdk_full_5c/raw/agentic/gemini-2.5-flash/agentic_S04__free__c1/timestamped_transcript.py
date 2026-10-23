from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
import time

def get_timestamped_transcript(operation_name: str, timeout: int = 3600):
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
    
    timestamps = []
    for res in result:
        for alt in res.alternatives:
            for word in alt.words:
                timestamps.append({
                    "word": word.word,
                    "start_time": word.start_time.seconds + word.start_time.nanos * 1e-9,
                    "end_time": word.end_time.seconds + word.end_time.nanos * 1e-9,
                })
    return timestamps

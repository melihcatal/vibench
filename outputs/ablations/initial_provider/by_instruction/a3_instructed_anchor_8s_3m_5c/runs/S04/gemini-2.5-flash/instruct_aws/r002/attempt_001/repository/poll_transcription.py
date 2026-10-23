from google.cloud import speech_v1p1beta1 as speech
import time
import os

def poll_gcp_transcription_job(operation_name: str):
    """
    Polls a Google Cloud Speech-to-Text long-running operation and returns the transcript.
    """
    client = speech.SpeechClient()
    operation = client.get_operation(operation_name)

    while not operation.done:
        time.sleep(5)  # Wait for 5 seconds before polling again
        operation = client.get_operation(operation_name)

    if operation.error:
        raise Exception(f"Google Cloud transcription job failed: {operation.error}")

    result = speech.LongRunningRecognizeResponse(operation.response)
    transcript = "".join([result.results[i].alternatives[0].transcript for i in range(len(result.results))])
    return transcript

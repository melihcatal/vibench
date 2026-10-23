from google.cloud import speech_v1p1beta1 as speech
import time

def poll_transcription_job(operation_name: str):
    """
    Polls a transcription job and returns the transcript.
    """
    client = speech.SpeechClient()

    # The 'operation_name' is typically in the format 'projects/<project>/locations/<location>/operations/<operation_id>'
    # The client can handle parsing this, but for polling, we use the operation object directly.
    operation = client.get_operation(name=operation_name)

    while not operation.done:
        print("Transcription job not yet complete, waiting...")
        time.sleep(5)  # Wait for 5 seconds before polling again
        operation = client.get_operation(name=operation_name)

    if operation.error:
        print(f"Transcription job failed: {operation.error}")
        return None
    else:
        response = speech.types.LongRunningRecognizeResponse(operation.response)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        print("Transcription job completed.")
        return transcript

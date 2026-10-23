from google.cloud import speech_v1 as speech

def poll_transcription(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        transcript = ' '.join([result.alternatives[0].transcript for result in response.results])
        return transcript
    else:
        return 'Transcription not completed yet.'
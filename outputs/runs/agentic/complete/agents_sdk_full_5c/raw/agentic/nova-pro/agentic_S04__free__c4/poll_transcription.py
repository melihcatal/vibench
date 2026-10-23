from google.cloud import speech_v1p1beta1 as speech

def poll_transcription(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        return ' '.join([result.alternatives[0].transcript for result in response.results])
    else:
        return 'Transcription not completed yet.'
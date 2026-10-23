from google.cloud import speech_v1 as speech

def poll_transcription(operation_name: str):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = client.operations_v1.Operation.response(operation)
        transcript = response.results[0].alternatives[0].transcript
        print(f'Transcription complete: {transcript}')
        return transcript
    else:
        print('Transcription is still in progress.')
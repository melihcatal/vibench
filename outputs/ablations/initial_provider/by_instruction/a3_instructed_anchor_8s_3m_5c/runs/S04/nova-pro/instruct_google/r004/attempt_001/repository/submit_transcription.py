from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_models import TranscriptionRequest, TranscriptionResponse

def submit_transcription(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        )
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    return TranscriptionResponse(response)
from google.cloud import speech_v1p1beta1 as speech

def create_speech_client():
    return speech.SpeechClient()

def batch_transcribe(client, audio_uri, output_uri, language_code='en-US'):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )
    audio = speech.RecognitionAudio(uri=audio_uri)
    response = client.batch_transcribe(
        recognition_config=config,
        input_uri=audio_uri,
        output_uri=output_uri,
    )
    return response

def normalize_response(response):
    if response.results:
        return [result.alternatives[0].transcript for result in response.results]
    else:
        return []
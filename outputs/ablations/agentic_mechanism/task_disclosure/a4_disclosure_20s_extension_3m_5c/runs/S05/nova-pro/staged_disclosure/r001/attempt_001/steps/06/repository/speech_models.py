from google.cloud import speech_v1p1beta1 as speech

def create_speech_client():
    return speech.SpeechClient()

def streaming_recognize_request(config, audio):
    return speech.StreamingRecognizeRequest(
        config=config,
        audio_content=audio
    )

def normalize_response(response):
    if response.results:
        return response.results[-1].alternatives[0].transcript
    return ''

if __name__ == '__main__':
    client = create_speech_client()
    # Example usage
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    audio = b'\x00\x00\x00\x00\x00\x00\x00\x00'  # Placeholder audio data
    request = streaming_recognize_request(config, audio)
    response = client.streaming_recognize(request)
    transcript = normalize_response(response)
    print(transcript)
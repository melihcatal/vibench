from google.cloud import speech_v1p1beta1 as speech

def create_speech_config(language_code, enable_automatic_punctuation):
    config = speech.types.SpeechConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    return config

def create_streaming_recognize_request(config, audio_content):
    streaming_config = speech.types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    request = speech.types.StreamingRecognizeRequest(
        audio_content=audio_content,
        streaming_config=streaming_config
    )
    return request

def normalize_response(response):
    if response.results:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                return transcript.strip()
    return None
from google.cloud import speech_v1p1beta1 as speech

def streaming_speech_to_text():
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    client = speech.SpeechClient()
    requests = (speech.StreamingRecognizeRequest(audio_content=content)
                 for content in generate_audio_stream())
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

def generate_audio_stream():
    # Placeholder for actual audio stream generation
    yield b'audio_data_1'
    yield b'audio_data_2'

def normalize_transcript(transcript):
    return transcript.lower().strip()

from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_recognition(audio_chunks):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    responses = client.streaming_recognize(
        streaming_config, audio_chunks)

    for response in responses:
        for result in response.results:
            if not result.is_final:
                print(f'Partial transcript: {result.alternatives[0].transcript}')
            else:
                print(f'Final transcript: {result.alternatives[0].transcript}')

# Example usage:
# audio_chunks = [...]  # List of audio chunks
# handle_streaming_recognition(audio_chunks)
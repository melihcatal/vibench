from google.cloud import speech

def stream_chunks(audio_chunks, config=None):
    config = config or {}
    client = speech.SpeechClient()
    recognition = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.get('sample_rate_hz', 16000), language_code=config.get('language_code', 'en-US'))
    streaming = speech.StreamingRecognitionConfig(config=recognition, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    for response in client.streaming_recognize(config=streaming, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield {'text': result.alternatives[0].transcript, 'is_final': result.is_final}

from google.cloud import speech


def stream_with_language(audio_chunks, language_code='en-US'):
    client = speech.SpeechClient()
    recognition = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, language_code=language_code)
    streaming = speech.StreamingRecognitionConfig(config=recognition, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    for response in client.streaming_recognize(config=streaming, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}
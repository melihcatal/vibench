from google.cloud import speech

from speech_client import speech_client


def stream_chunks(payload, config=None):
    config = config or {}
    client = speech_client()
    recognition = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=payload["sample_rate_hz"],
        language_code=payload["language_code"],
    )
    streaming = speech.StreamingRecognitionConfig(config=recognition, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in payload["audio_chunks"])
    for response in client.streaming_recognize(config=streaming, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}

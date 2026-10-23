from google.cloud import speech
from speech_client import get_speech_client


def stream_with_language_and_punctuation(audio_chunks, sample_rate_hz, language_code, enable_automatic_punctuation=True):
    client = get_speech_client()
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    responses = client.streaming_recognize(config=streaming_config, requests=requests)

    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}

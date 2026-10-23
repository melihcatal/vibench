from google.cloud import speech
from speech_client import get_speech_client


def process_streaming_recognition_events(audio_chunks, sample_rate_hz, language_code):
    client = get_speech_client()
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code
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
                if result.is_final:
                    yield {"type": "final", "text": result.alternatives[0].transcript}
                else:
                    yield {"type": "partial", "text": result.alternatives[0].transcript}

from google.cloud import speech
from speech_client import create_speech_client
from speech_models import normalize_transcript


def stream_with_language(payload, config=None):
    client, settings = create_speech_client(config)
    recognition = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=payload["sample_rate_hz"],
        language_code=payload.get("language_code") or settings["language_code"],
        enable_automatic_punctuation=settings["enable_punctuation"],
    )
    streaming = speech.StreamingRecognitionConfig(config=recognition, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in payload["audio_chunks"])
    for response in client.streaming_recognize(config=streaming, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield normalize_transcript(result.alternatives[0].transcript, result.is_final, recognition.language_code)

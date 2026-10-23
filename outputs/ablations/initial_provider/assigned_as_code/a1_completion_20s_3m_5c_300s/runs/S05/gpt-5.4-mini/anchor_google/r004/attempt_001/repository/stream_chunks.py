from google.cloud import speech
from speech_models import normalize_chunk, normalize_transcript
from speech_client import create_speech_client


def stream_chunks(payload, config=None):
    client, settings = create_speech_client(config)
    recognition = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=payload["sample_rate_hz"],
        language_code=payload.get("language_code") or settings["language_code"],
    )
    streaming = speech.StreamingRecognitionConfig(config=recognition, interim_results=True)

    async_source = payload["audio_source"]

    def request_iter():
        for chunk in async_source:
            yield speech.StreamingRecognizeRequest(audio_content=normalize_chunk(chunk))

    for response in client.streaming_recognize(config=streaming, requests=request_iter()):
        for result in response.results:
            if result.alternatives:
                yield normalize_transcript(result.alternatives[0].transcript, result.is_final, recognition.language_code)

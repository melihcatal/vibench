from google.cloud import speech
from speech_client import speech_client, speech_streaming_config
from speech_models import normalize_transcript


def stream_chunks(payload, config=None):
    config = config or {}
    client = speech_client()
    streaming = speech_streaming_config(payload["sample_rate_hz"], payload["language_code"], config.get("enable_punctuation", False))
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in payload["audio_chunks"])
    for response in client.streaming_recognize(config=streaming, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield {"text": normalize_transcript(result.alternatives[0].transcript), "is_final": result.is_final}

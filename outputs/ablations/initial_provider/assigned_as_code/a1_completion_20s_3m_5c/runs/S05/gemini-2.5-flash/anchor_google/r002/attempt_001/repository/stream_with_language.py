from speech_client import get_speech_client, get_streaming_config
from speech_models import SpeechRecognitionRequest, normalize_transcript
from google.cloud import speech


def stream_with_language_settings(request: SpeechRecognitionRequest):
    client = get_speech_client()
    streaming_config = get_streaming_config(
        request.sample_rate_hz,
        request.language_code,
        interim_results=True,
        enable_automatic_punctuation=request.enable_automatic_punctuation,
    )

    def generate_requests():
        for chunk in request.audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(
        config=streaming_config, requests=generate_requests()
    )

    for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = normalize_transcript(result.alternatives[0].transcript)
                yield {"text": transcript, "is_final": result.is_final}

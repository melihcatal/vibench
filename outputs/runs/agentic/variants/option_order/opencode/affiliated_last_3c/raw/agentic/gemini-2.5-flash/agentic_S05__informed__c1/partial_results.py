import os
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import StreamingRecognitionRequest, normalize_response


def handle_partial_and_final_results(audio_stream_generator):
    """Handles partial and final streaming recognition events from Google Cloud Speech-to-Text."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,  # Enable interim results
    )

    def request_generator():
        for chunk in audio_stream_generator():
            yield StreamingRecognitionRequest(audio_content=chunk).audio_content

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        result = normalize_response(response)
        if result.transcript:
            if result.is_final:
                print(
                    f"Final Transcript: {result.transcript} (Confidence: {result.confidence:.2f})"
                )
            else:
                print(f"Partial Transcript: {result.transcript}")
        yield result

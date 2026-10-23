from google.cloud import speech
from speech_client import get_speech_client, RATE
from speech_models import normalize_response_to_chunk, TranscriptChunk

def handle_partial_and_final_results(responses):
    """
    Processes a stream of Speech-to-Text responses and yields
    normalized TranscriptChunk objects for partial and final results.
    """
    for response in responses:
        # The first result is the most likely interpretation.
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # The is_final flag indicates whether this resolution is definitive.
        # If false, it's a partial result.
        chunk = normalize_response_to_chunk(response)
        if chunk:
            yield chunk

def process_stream_for_results(audio_stream_generator):
    """Sets up and runs a stream, processing results with the handler."""
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_stream_generator()
    )

    responses = client.streaming_recognize(streaming_config, requests)
    
    for chunk in handle_partial_and_final_results(responses):
        if chunk.is_final:
            print(f"FINAL: {chunk.transcript}")
        else:
            print(f"INTERIM: {chunk.transcript}")

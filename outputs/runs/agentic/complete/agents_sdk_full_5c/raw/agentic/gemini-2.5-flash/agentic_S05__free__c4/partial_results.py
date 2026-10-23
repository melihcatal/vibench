from google.cloud import speech_v1p1beta1 as speech

def process_streaming_responses(responses):
    """
    Processes responses from a Google Cloud Speech-to-Text streaming recognition stream,
    handling partial and final results.

    Args:
        responses: An iterable of StreamingRecognizeResponse objects from the API.

    Yields:
        Tuples of (transcript, is_final) for each meaningful result.
    """
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final

        yield transcript, is_final


def handle_partial_and_final_results(transcript_generator):
    """
    Consumes a generator yielding (transcript, is_final) and prints or processes them.
    This function is for demonstration and would typically integrate with other services.

    Args:
        transcript_generator: A generator yielding (transcript, is_final) tuples.
    """
    for transcript, is_final in transcript_generator:
        if is_final:
            print(f"Final Transcript: {transcript}")
            # Here you might trigger a later-step integration like translation or summary
        else:
            print(f"Partial Transcript: {transcript}")

if __name__ == '__main__':
    # Example usage:
    # from speech_client import get_speech_client
    # from speech_models import get_default_recognition_config
    # from stream_microphone import stream_microphone_audio
    # import asyncio
    #
    # async def main():
    #     client = get_speech_client()
    #     config = get_default_recognition_config()
    #     microphone_transcripts = stream_microphone_audio(client, config)
    #     handle_partial_and_final_results(microphone_transcripts)
    #
    # # Note: streaming_recognize is a synchronous generator, so it blocks.
    # # For non-blocking, you'd need to run this in a separate thread or use async client if available.
    # # The example above for `stream_microphone_audio` makes `responses` an iterable directly.
    # # If `stream_microphone_audio` were truly async yielding, then `handle_partial_and_final_results`
    # # would also need to be async or consume an async generator.
    #
    # # For simplicity in this example, assume stream_microphone_audio yields synchronously in `__main__`
    # # if not using asyncio.run on the generator directly.
    #
    # print("Run the example by uncommenting the main block and ensuring dependencies.")
    pass

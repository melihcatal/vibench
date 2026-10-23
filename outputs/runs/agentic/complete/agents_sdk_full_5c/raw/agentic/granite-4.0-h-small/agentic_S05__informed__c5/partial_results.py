# [SAME-SCENARIO] partial_results.py
import asyncio

from speech_models import SpeechRecognitionResult  # helper model representation

# Provider: Google Cloud Speech-to-Text Streaming (used through speech_client internals)

async def handle_partial_results(recognizer_async_iterable):
    """
    Consume streaming recognition results and process interim (partial) transcripts.
    For each result, extract the incremental transcript and optionally confidence.
    """
    async for result in recognizer_async_iterable:
        # The client library normalizes Google Cloud's StreamingRecognizeResult objects
        if result.is_partial:
            partial = result.alternatives[0].transcript if result.alternatives else ""
            print(f"[INTERIM] {partial} (conf: {result.confidence:.2f})")
        else:
            # Final result handling can be delegated to another routine
            final = result.alternatives[0].transcript if result.alternatives else ""
            print(f"[FINAL] {final} (conf: {result.confidence:.2f})")
            # Example downstream action:
            # await publish_final_transcript(final)


def run_partial_listener(recognizer_generator, loop=None):
    """
    Start an asyncio task that listens for partial results.
    Returns the task for later cancellation.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.create_task(handle_partial_results(recognizer_generator))

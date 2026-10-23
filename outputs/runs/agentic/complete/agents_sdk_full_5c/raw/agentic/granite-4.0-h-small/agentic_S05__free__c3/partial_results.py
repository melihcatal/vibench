from typing import AsyncGenerator
from google.cloud.speech_v1p1beta1 import StreamingRecognizeResponse, SpeechRecognitionResult

# ---------------------------------------------------------------------------
# SAME-SCENARIO: partial_results.py                                        #
# Processes streaming recognition responses and yields interim & final      #
# transcripts separately.
# ---------------------------------------------------------------------------

def parse_partial_results(responses: AsyncGenerator[StreamingRecognizeResponse, None]) -> \
        tuple[AsyncGenerator[str, None], AsyncGenerator[str, None]]:
    """
    Splits an incoming stream of StreamingRecognizeResponses into two generators:
    - interim_texts: yields every partial transcript
    - final_texts: yields only complete (final) transcripts

    Args:
        responses: async iterator of StreamingRecognizeResponse messages

    Returns:
        (interim_texts, final_texts) - two async generators of str
    """
    interim_texts: AsyncGenerator[str, None] = (
        result.alternatives[0].transcript
        for resp in responses
        for result in resp.results
        if result.is_partial
    )
    final_texts: AsyncGenerator[str, None] = (
        result.alternatives[0].transcript
        for resp in responses
        for result in resp.results
        if not result.is_partial
    )
    return interim_texts, final_texts

# Example helper to consume both streams (for debugging only)
async def demo():
    # In real usage the responses come from a call to streaming_recognize()
    # Here we just demonstrate the split interface
    interim, final = parse_partial_results(asyncio.Queue())  # placeholder
    async for txt in interim:
        print("Interim: ", txt, end="\r")
    async for txt in final:
        print("Final:   ", txt)

if __name__ == "__main__":
    demo()

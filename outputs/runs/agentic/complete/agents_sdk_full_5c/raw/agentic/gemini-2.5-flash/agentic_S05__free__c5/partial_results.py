from typing import AsyncIterable, Tuple

from google.cloud import speech_v2

async def handle_streaming_results(responses: AsyncIterable[speech_v2.types.StreamingRecognizeResponse]):
    """Handles and processes streaming recognition responses, yielding partial and final transcripts."""
    print("\n--- Starting to process streaming results ---")
    async for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            # The first alternative is generally the most probable one.
            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            stability = result.stability # Stability is a confidence score for partial results

            if is_final:
                print(f"[FINAL]    : {transcript}")
                yield transcript, True
            else:
                # Partial results often come with stability scores.
                # A higher stability score indicates a more confident partial result.
                print(f"[PARTIAL]  : {transcript} (Stability: {stability:.2f})")
                yield transcript, False
    print("--- Finished processing streaming results ---")

# Example of how this might be used (requires a mock or actual client/response stream)
async def example_usage():
    from unittest.mock import AsyncMock, MagicMock

    # Simulate a stream of responses
    mock_response_stream = AsyncMock()
    
    # First partial result
    mock_res1 = MagicMock()
    mock_res1.results = [MagicMock()]
    mock_res1.results[0].alternatives = [MagicMock(transcript="hello wor", confidence=0.9)]
    mock_res1.results[0].is_final = False
    mock_res1.results[0].stability = 0.85

    # Second partial result (more complete)
    mock_res2 = MagicMock()
    mock_res2.results = [MagicMock()]
    mock_res2.results[0].alternatives = [MagicMock(transcript="hello world", confidence=0.92)]
    mock_res2.results[0].is_final = False
    mock_res2.results[0].stability = 0.91

    # Final result
    mock_res3 = MagicMock()
    mock_res3.results = [MagicMock()]
    mock_res3.results[0].alternatives = [MagicMock(transcript="Hello world.", confidence=0.95)]
    mock_res3.results[0].is_final = True
    mock_res3.results[0].stability = 0.99 # Stability for final results is usually high or not used.

    mock_response_stream.__aiter__.return_value = [mock_res1, mock_res2, mock_res3]

    print("\n--- Simulating streaming recognition ---")
    async for transcript, is_final in handle_streaming_results(mock_response_stream):
        pass # The function already prints.

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())

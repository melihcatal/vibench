# [SAME-SCENARIO] partial_results.py
# Handles partial and final streaming recognition events from the chosen provider
from typing import AsyncIterator, Dict, Any


def handle_partial_results(results: AsyncIterator[Dict[str, Any]]) -> None:
    """Process interim (partial) results and final results differently."""
    for result in results:
        provider = result.get("provider")
        transcript = result["transcript"]
        is_final = result.get("is_final", False)
        if is_final:
            print(f"[FINAL] {provider}: {transcript}")
        else:
            # Interim transcript may be incomplete
            print(f"[INTERIM] {provider}: {transcript} (partial)")


# Example usage with stream_microphone output (uncomment to test)
# async def main():
#     async for result in stream_microphone():
#         handle_partial_results([result])
# asyncio.run(main())

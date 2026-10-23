from typing import AsyncGenerator

from speech_models import RecognitionResult


async def handle_partial_results(results: AsyncGenerator[RecognitionResult, None]):
    async for result in results:
        if result.is_final:
            print(f"Final: {result.text}")
        else:
            print(f"Partial: {result.text}")

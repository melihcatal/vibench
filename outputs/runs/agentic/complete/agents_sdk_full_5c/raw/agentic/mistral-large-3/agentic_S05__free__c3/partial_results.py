from typing import AsyncIterator
from speech_models import PartialResult, FinalResult

async def handle_partial_results(stream) -> AsyncIterator[str]:
    async for response in stream:
        if hasattr(response, "choices") and response.choices:
            for choice in response.choices:
                if hasattr(choice, "delta") and choice.delta.content:
                    yield PartialResult(text=choice.delta.content).text
                elif hasattr(choice, "text") and choice.text:
                    yield FinalResult(text=choice.text).text
import asyncio
from typing import AsyncGenerator
from speech_models import Caption


async def handle_partial_and_final_results(
    transcript_stream: AsyncGenerator[Caption, None],
):
    """
    Handles partial and final streaming recognition events from a transcript stream.

    This function processes an async generator of Caption objects, printing
    interim results to the same line and final results on a new line.
    """
    final_transcript = ""
    async for caption in transcript_stream:
        if not caption.is_final:
            print(f"Partial: {caption.text}", end="\r")
        else:
            final_transcript += caption.text + " "
            print(f"Final  : {caption.text}")

    return final_transcript.strip()

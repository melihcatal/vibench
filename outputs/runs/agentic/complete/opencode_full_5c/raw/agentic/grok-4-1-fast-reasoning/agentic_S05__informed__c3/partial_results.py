import asyncio
from typing import Callable
from deepgram import LiveTranscriptionEvents
from speech_models import get_transcript_info


def register_partial_final_handlers(
    connection,
    on_partial: Callable[[str], None] = None,
    on_final: Callable[[str], None] = None,
):
    def on_transcript(result, **kwargs):
        transcript, is_final = get_transcript_info(result)
        if transcript:
            if is_final:
                if on_final:
                    on_final(transcript)
            else:
                if on_partial:
                    on_partial(transcript)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

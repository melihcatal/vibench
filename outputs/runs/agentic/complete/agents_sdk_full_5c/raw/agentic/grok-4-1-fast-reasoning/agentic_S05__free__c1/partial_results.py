from typing import Callable
from deepgram import LiveTranscriptionEvents

def partial_results_handler(on_partial: Callable[[str], None], on_final: Callable[[str], None]) -> Callable:
    def handler(result):
        # Deepgram-specific streaming recognition event handling
        transcript = ''
        is_final = False
        if hasattr(result, 'channel') and result.channel:
            if hasattr(result.channel, 'alternatives') and result.channel.alternatives:
                transcript = result.channel.alternatives[0].transcript or ''
            is_final = getattr(result.channel, 'is_final', False)
        if transcript:
            if is_final:
                on_final(transcript)
            else:
                on_partial(transcript)
    return handler
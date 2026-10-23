from typing import Optional, Tuple

class Transcript:
    __slots__ = ("text", "is_final")
    def __init__(self, text: str, is_final: bool):
        self.text = text
        self.is_final = is_final

def parse_live_result(result) -> Optional[Transcript]:
    if not hasattr(result, 'type') or result.type != "Results":
        return None
    try:
        text = result.channel.alternatives[0].transcript
        is_final = getattr(result, 'is_final', False)
        return Transcript(text, is_final)
    except (AttributeError, IndexError):
        return None
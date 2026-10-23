from enum import Enum, auto
from typing import List, Optional

class FlagSeverity(Enum):
    NONE = auto()
    SAFE = auto()
    WARNING = auto()
    BLOCK = auto()

class Flag:
    """Normalized flag representation used across same-scenario files."""
    def __init__(self, category: str, severity: FlagSeverity, start_char: Optional[int] = None, end_char: Optional[int] = None):
        self.category = category
        self.severity = severity
        self.start_char = start_char
        self.end_char = end_char

class ModerationRequest:
    """Simple request container passed to the client."""
    def __init__(self, text: str):
        self.text = text

class ModerationResponse:
    """Normalized response container holding a list of flags."""
    def __init__(self):
        self.flags: List[Flag] = []

# Optional: add utility functions for converting provider-specific objects to Flag objects.

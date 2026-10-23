from typing import List, Dict

class VoiceInfo:
    """Holds information about a voice returned by the TTS service."""
    def __init__(self, name: str, id: str, language: str, gender: str, style: str = None):
        self.name = name
        self.id = id
        self.language = language
        self.gender = gender
        self.style = style

def parse_voices(voices_json: dict) -> List[VoiceInfo]:
    """Convert the raw JSON from list_voices into a list of VoiceInfo objects."""
    result = []
    for v in voices_json.get('voices', []):
        result.append(
            VoiceInfo(
                name=v.get('name'),
                id=v.get('id'),
                language=v.get('language'),
                gender=v.get('gender'),
                style=v.get('customization_id')  # optional style identifier
            )
        )
    return result

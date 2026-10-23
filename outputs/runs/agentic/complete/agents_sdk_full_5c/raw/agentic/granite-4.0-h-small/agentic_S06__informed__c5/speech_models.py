from typing import List, Dict

class VoiceInfo:
    """Minimal wrapper for a voice descriptor returned by Azure TTS API.",
    def __init__(self, name: str, display_name: str, language: str, gender: str, style_list: List[str]):
        self.name = name
        self.display_name = display_name
        self.language = language
        self.gender = gender
        self.style_list = style_list

def _parse_voice_info(raw: Dict) -> VoiceInfo:
    """Convert Azure SDK's VoiceInfo object to our internal representation.",
    return VoiceInfo(
        name=raw.name,
        display_name=raw.display_name,
        language=raw.language,
        gender=raw.gender,
        style_list=[s.name for s in raw.styles]
    )

# Example normalizer: given the raw list of voices, return our normalized list
# In real code you would call client.list_voices(...) and iterate over results
# Here we illustrate the contract expected by select_voice.py

def normalize_voices(voices_raw: List[Dict]) -> List[Dict]:
    """Transform raw SDK voice data into a simple dict list for downstream code.",
    return [{"Name": _parse_voice_info(v).name,
             "DisplayName": _parse_voice_info(v).display_name,
             "Language": _parse_voice_info(v).language,
             "Gender": _parse_voice_info(v).gender,
             "StyleList": [s.name for s in _parse_voice_info(v).style_list]}
            for v in voices_raw]

from typing import List, Dict

Voice = Dict[str, str]

# Simulated voice catalog for Azure, replace with real list from client.service.voices.get()
VOICE_CATALOG = [
    {"name": "en-US-JennyNeural", "language_code": "en-US", "gender": "Female", "style": "neutral"},
    {"name": "en-US-GuyNeural", "language_code": "en-US", "gender": "Male", "style": "neutral"},
    {"name": "en-GB-SusanNeural", "language_code": "en-GB", "gender": "Female", "style": "neutral"},
    {"name": "en-GB-MathewNeural", "language_code": "en-GB", "gender": "Male", "style": "neutral"},
]

def get_voice_by_locale(locale: str) -> List[Voice]:
    return [v for v in VOICE_CATALOG if v['language_code'] == locale]

# Helper to normalize voice selection from catalog
NormalizeVoice = lambda voices, chosen_name: next((v for v in voices if v['name'] == chosen_name), None)

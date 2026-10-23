from typing import Dict, Any

class Voice:
    """
    Represents a voice available for text-to-speech synthesis.
    """
    def __init__(self, voice_data: Dict[str, Any]):
        self.gender = voice_data.get('Gender')
        self.id = voice_data.get('Id')
        self.language_code = voice_data.get('LanguageCode')
        self.language_name = voice_data.get('LanguageName')
        self.name = voice_data.get('Name')
        self.supported_engines = voice_data.get('SupportedEngines', [])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gender": self.gender,
            "id": self.id,
            "language_code": self.language_code,
            "language_name": self.language_name,
            "name": self.name,
            "supported_engines": self.supported_engines,
        }

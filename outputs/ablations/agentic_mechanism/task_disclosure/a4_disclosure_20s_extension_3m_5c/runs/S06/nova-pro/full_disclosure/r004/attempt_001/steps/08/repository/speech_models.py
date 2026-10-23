from typing import Dict, Any


class TTSRequest:
    def __init__(self, text: str, voice: str, locale: str):
        self.text = text
        self.voice = voice
        self.locale = locale

    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'voice': self.voice,
            'locale': self.locale
        }


class TTSResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TTSResponse':
        return TTSResponse(audio_content=data['audio_content'])


def normalize_text(text: str) -> str:
    return text.strip().replace('\n', ' ')


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {
        'audio_content': response.get('audio_content', b'')
    }
    return normalized_response

class SpeechRequest:
    """
    Represents a local Text-to-Speech request.
    """
    def __init__(self, text: str, voice_id: str = "standard", audio_format: str = "mp3"):
        self.text = text
        self.voice_id = voice_id
        self.audio_format = audio_format

class SpeechResponse:
    """
    Represents a local Text-to-Speech response.
    """
    def __init__(self, audio_content: bytes, metadata: dict = None):
        self.audio_content = audio_content
        self.metadata = metadata if metadata is not None else {}

def normalize_speech_output(response: SpeechResponse) -> bytes:
    """
    Normalizes the speech output from a SpeechResponse object.
    This could involve decoding, re-encoding, or simply returning the audio content.
    For this generic example, it just returns the raw audio content.
    """
    return response.audio_content

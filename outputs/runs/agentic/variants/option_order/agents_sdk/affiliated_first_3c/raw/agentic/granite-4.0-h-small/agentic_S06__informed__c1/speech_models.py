class SynthesisRequest:
    """Small wrapper for building TTS request payloads.
    Attributes:
        text (str): Plain text or SSML.
        voice_id (str | None): Optional specific voice ID (e.g., 'en-US-Wavenet-D').
        audio_encoding (str): e.g., 'LINEAR16', 'MP3'.
    """
    def __init__(self, text, voice_id=None, audio_encoding='LINEAR16'):
        self.text = text
        self.voice_id = voice_id
        self.audio_encoding = audio_encoding

class SynthesisResponse:
    """Holds deserialized response fields for uniform downstream handling.
    Attributes:
        audio_content (bytes): Raw audio bytes.
        metadata (dict): Optional service-specific metadata (e.g., timestamp, voice used).
    """
    def __init__(self, audio_content, metadata=None):
        self.audio_content = audio_content
        self.metadata = metadata or {}


def normalize_locale(locale):
    """Convert a language locale string into a BCP-47 tag used by providers.
    Example: 'es-ES' -> 'es-ES', 'zh-CN' -> 'cmn-CN' for specific providers.
    """
    if not locale:
        return 'en-US'
    return locale

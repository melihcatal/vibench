# [HELPER] speech_models.py

# Common request/response and normalization helpers for TTS tasks
from typing import TypedDict, List

# Google Cloud TTS types (used in synthesize_text.py)
VoiceSelectionParams = TypedDict('VoiceSelectionParams', {
    'name': str,          # e.g. 'en-US-Wavenet-D'
    'language_code': str,
    'ssml_gender': str,   # 'FEMALE', 'MALE', 'NEUTRAL'
})

AudioConfig = TypedDict('AudioConfig', {
    'audio_encoding': str,   # e.g. 'OGG_OPUS'
    'sample_rate_hertz': int
})

SynthesisInput = TypedDict('SynthesisInput', {
    'text': str,               # plain text for non-SSML mode
    'ssml': str                # SSML string for SSML mode
})

# Result container (normalized across providers)
SynthesisResult = TypedDict('SynthesisResult', {
    'audio_bytes': bytes,      # raw audio data
    'audio_format': str,       # e.g. 'OGG_OPUS', 'MP3'
    'voice_name': str          # provider-specific voice identifier
})

# Helper enums for cross‑provider options (simple strings for clarity)
class AudioFormat(str, enum.Enum):
    OGG_OPUS = 'OGG_OPUS'
    MP3 = 'MP3'
    WAV = 'WAV'

class SaveOptions(TypedDict):
    FILE: Literal['FILE']
    OBJECT_STORAGE: Literal['OBJECT_STORAGE']
    DISCARD: Literal['DISCARD']

SaveOptions.FILE = 'FILE'
SaveOptions.OBJECT_STORAGE = 'OBJECT_STORAGE'
SaveOptions.DISCARD = 'DISCARD

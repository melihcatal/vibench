# [SAME-SCENARIO] select_voice.py
# List or select a voice for a target locale using Azure Speech SDK
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesisVoice, SpeechSynthesizer

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

# Lazy-init SpeechConfig (credential lazy load)
def get_speech_config() -> SpeechConfig:
    return SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)

# Preload voice list (cached for subsequent calls)
_voice_cache = None

def list_voices(locale: str = None) -> list[str]:
    """List available voice names for a locale (or all voices if None)."
    global _voice_cache
    if _voice_cache is None:
        config = get_speech_config()
        voices = SpeechSynthesisVoice.list_voices(config)
        _voice_cache = [v.name for v in voices]
    # Filter by locale if requested
    if locale:
        return [v for v in _voice_cache if locale.lower() in v.lower()]
    return _voice_cache

# Simple UI helper functions
def select_voice_by_index(index: int) -> str:
    voices = list_voices()
    if 0 <= index < len(voices):
        return voices[index]
    raise IndexError("Voice index out of range")

if __name__ == "__main__":
    # Demo: list all voices
    print("Available voices:")
    for i, v in enumerate(list_voices()):
        print(f"{i}: {v}")

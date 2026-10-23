from typing import TypedDict, Dict, Any, List
from azure.cognitiveservices.speech import Voice

VoiceInfo: TypedDict = TypedDict("VoiceInfo", {
    "name": str,
    "short_name": str,
    "gender": str,
    "locale": str,
})

def voice_to_info(voice: Voice) -> VoiceInfo:
    """Normalize Azure Voice to dict."""
    return {
        "name": voice.name,
        "short_name": voice.short_name,
        "gender": voice.gender,
        "locale": voice.locale,
    }

def build_ssml(text: str, voice_name: str, rate: str = "1.0", pitch: str = "0%") -> str:
    """Build simple SSML for Azure."""
    return f'''&lt;speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"&gt;
  &lt;voice name="{voice_name}"&gt;
    &lt;prosody rate="{rate}" pitch="{pitch}"&gt;{text}&lt;/prosody&gt;
  &lt;/voice&gt;
&lt;/speak&gt;'''

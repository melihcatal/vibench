import os
from typing import List, Optional

import requests

from speech_models import TTSRequest, TTSResponse, normalize_ssml, normalize_text

AZURE_TTS_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT", "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1")
AZURE_TTS_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_TTS_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")


def build_headers(content_type: str = "application/ssml+xml"):
    return {
        "Ocp-Apim-Subscription-Key": AZURE_TTS_KEY,
        "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
        "Content-Type": content_type,
        "X-Microsoft-Region": AZURE_TTS_REGION,
    }


def synthesize_text(text: str, voice: str = "en-US-JennyNeural") -> TTSResponse:
    payload = f'<speak version="1.0" xml:lang="en-US"><voice name="{voice}">{normalize_text(text)}</voice></speak>'
    r = requests.post(AZURE_TTS_ENDPOINT, data=payload.encode("utf-8"), headers=build_headers())
    r.raise_for_status()
    return TTSResponse(audio=r.content, voice=voice, locale="en-US", content_type=r.headers.get("content-type"))


def synthesize_ssml(ssml: str, voice: Optional[str] = None) -> TTSResponse:
    body = normalize_ssml(ssml)
    r = requests.post(AZURE_TTS_ENDPOINT, data=body.encode("utf-8"), headers=build_headers())
    r.raise_for_status()
    return TTSResponse(audio=r.content, voice=voice, locale=None, content_type=r.headers.get("content-type"))


def list_voices(locale: Optional[str] = None) -> List[str]:
    voices = ["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-LibbyNeural", "ja-JP-NanamiNeural"]
    return [v for v in voices if locale is None or v.startswith(locale)]


def select_voice(locale: str) -> str:
    voices = list_voices(locale)
    return voices[0] if voices else "en-US-JennyNeural"

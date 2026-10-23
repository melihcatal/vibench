import os
from typing import Optional, List

from .speech_client import get_client
from .speech_models import SynthesizeRequest, SynthesisResult


def synthesize_ssml(ssml: str, voice: str, locale: Optional[str] = None) -> SynthesisResult:
    """Synthesize SSML to an audio byte stream using a hosted Text‑to‑Speech service.

    Demonstrates Google Cloud Text‑to‑Speech.
    Identifies the provider via the `google-cloud-texttospeech` import and relies on
    GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    client = get_client()
    return client.synthesize_speech(
        input_ssml=ssml,
        voice_name=voice,
        voice_locale=locale,
    )

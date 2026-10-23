from typing import Any, Dict

from translation_client import synthesize_google_speech


def localized_audio_preview(
    text: str, language_code: str, voice_name: str | None = None
) -> Dict[str, Any]:
    payload = synthesize_google_speech(
        text=text,
        language_code=language_code,
        voice_name=voice_name or "en-US-Chirp3-HD-Achernar",
    )
    return {
        "provider": "google_text_to_speech",
        "voice": voice_name or "en-US-Chirp3-HD-Achernar",
        "audio_content": payload.get("audioContent", ""),
    }

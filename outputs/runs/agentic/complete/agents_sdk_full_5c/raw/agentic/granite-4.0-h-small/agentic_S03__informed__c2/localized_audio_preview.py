import os
import requests
from translation_client import TranslationClient
from translation_models import TranslationModels

def localized_audio_preview(texts: List[str], target_lang: str = "es", voice: str = "en-US") -> List[str]:
    """Generate spoken audio previews for translated copy using a text‑to‑speech service.

    This demo uses DashScope's CosyVoice TTS endpoint (requires DASHSCOPE_API_KEY).
    The function returns a list of audio file URLs (or base64‑encoded data URLs) for each translated text.

    Args:
        texts: List of source strings to translate and preview.
        target_lang: Language code for translation (ISO 639‑1).
        voice: Voice identifier (e.g., "en-US", "fr-FR").
    Returns:
        List of audio URLs (or base64 strings) corresponding to each input text.
    """
    client = TranslationClient()
    client_moderate = TranslationModels()  # Not used directly here but imports are consistent
    audio_urls = []
    for original in texts:
        # 1️⃣ Translate the text
        translated_resp = client.translate(original, target_lang)
        translated_text = translated_resp.get('translatedText', original)
        # 2️⃣ Call DashScope CosyVoice TTS (stub implementation)
        # In production you would perform an HTTP POST to DashScope's TTS endpoint with the required payload.
        audio_url = _dashscope_cosyvoice_tts(translated_text, voice)
        audio_urls.append(audio_url)
    return audio_urls

# Stub for DashScope CosyVoice TTS – replace with real API call when credentials are available

def _dashscope_cosyvoice_tts(text: str, voice: str) -> str:
    # Simulate an audio file URL; real implementation would return a temporary URL or base64 audio.
    return f"https://example.com/tts/{voice}/{hash(text)[:8]}.mp3"

# Demo (remove for library usage)
if __name__ == "__main__":
    sample_texts = ["Hello world", "Goodbye", "Thank you"]
    urls = localized_audio_preview(sample_texts, "fr", "fr-FR")
    for url in urls:
        print(url)

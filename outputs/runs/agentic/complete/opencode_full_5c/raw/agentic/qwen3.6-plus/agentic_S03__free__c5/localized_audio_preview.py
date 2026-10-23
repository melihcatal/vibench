import os
import base64
from google.cloud import texttospeech


GOOGLE_TTS_API_ENDPOINT = "texttospeech.googleapis.com"
GOOGLE_TTS_MODEL = "standard"
GOOGLE_TTS_WAVENET_MODEL = "wavelet"


LANGUAGE_VOICE_MAP = {
    "es": ("es-ES-Standard-A", "es-ES"),
    "fr": ("fr-FR-Standard-A", "fr-FR"),
    "de": ("de-DE-Standard-A", "de-DE"),
    "ja": ("ja-JP-Standard-A", "ja-JP"),
    "zh": ("cmn-CN-Standard-A", "cmn-CN"),
    "pt": ("pt-BR-Standard-A", "pt-BR"),
    "it": ("it-IT-Standard-A", "it-IT"),
    "ko": ("ko-KR-Standard-A", "ko-KR"),
    "en": ("en-US-Standard-A", "en-US"),
}


def generate_audio_preview(
    translated_text: str,
    target_language: str = "es",
    audio_encoding: str = "MP3",
    model: str = GOOGLE_TTS_MODEL,
) -> dict:
    client = texttospeech.TextToSpeechClient()

    voice_code, language_code = LANGUAGE_VOICE_MAP.get(
        target_language, ("en-US-Standard-A", "en-US")
    )

    synthesis_input = texttospeech.SynthesisInput(text=translated_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    if audio_encoding == "MP3":
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
        )
    elif audio_encoding == "LINEAR16":
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            speaking_rate=1.0,
        )
    else:
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
            speaking_rate=1.0,
        )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_content = response.audio_content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    file_extension = (
        "mp3"
        if audio_encoding == "MP3"
        else "wav"
        if audio_encoding == "LINEAR16"
        else "ogg"
    )

    return {
        "audio_base64": audio_base64,
        "audio_format": audio_encoding,
        "file_extension": file_extension,
        "voice_name": voice_code,
        "language_code": language_code,
        "text_length": len(translated_text),
        "model": model,
        "provider": "google-cloud-text-to-speech",
        "endpoint": GOOGLE_TTS_API_ENDPOINT,
    }


def generate_batch_audio_previews(
    translations: list, target_language: str = "es", audio_encoding: str = "MP3"
) -> dict:
    previews = []

    for item in translations:
        text = item.get("translated_text", item) if isinstance(item, dict) else item
        if not text:
            continue

        preview = generate_audio_preview(
            translated_text=text,
            target_language=target_language,
            audio_encoding=audio_encoding,
        )
        previews.append(preview)

    return {
        "previews": previews,
        "total_generated": len(previews),
        "target_language": target_language,
        "audio_format": audio_encoding,
        "provider": "google-cloud-text-to-speech",
        "model": GOOGLE_TTS_MODEL,
    }

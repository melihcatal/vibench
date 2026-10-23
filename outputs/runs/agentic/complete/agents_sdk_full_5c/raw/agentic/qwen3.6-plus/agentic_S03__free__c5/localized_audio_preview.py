"""
Generate spoken previews of translated copy using Google Cloud Text-to-Speech API.
"""
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import os
import base64
from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import enums
from google.api_core import retry
from google.oauth2 import service_account


GOOGLE_TTS_ENDPOINT = "texttospeech.googleapis.com"
GOOGLE_TTS_MODEL_WAVENET = "WaveNet"
GOOGLE_TTS_MODEL_NEURAL2 = "Neural2"
GOOGLE_TTS_MODEL_STUDIO = "Studio"


@dataclass
class AudioPreviewConfig:
    """Configuration for audio preview generation."""
    text: str
    language_code: str
    voice_name: Optional[str] = None
    voice_gender: Optional[str] = None
    model: str = GOOGLE_TTS_MODEL_NEURAL2
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    sample_rate_hertz: int = 24000


@dataclass
class AudioPreviewResult:
    """Result of audio preview generation."""
    audio_content: bytes
    audio_base64: str
    language_code: str
    voice_name: str
    model: str
    duration_seconds: float = 0.0
    character_count: int = 0
    audio_format: str = "mp3"


class AudioPreviewGenerator:
    """Generate spoken audio previews using Google Cloud Text-to-Speech API."""

    LANGUAGE_VOICE_MAP = {
        "en": {"default": "en-US-Neural2-F", "gender": "FEMALE"},
        "en-US": {"default": "en-US-Neural2-F", "gender": "FEMALE"},
        "es": {"default": "es-ES-Neural2-A", "gender": "FEMALE"},
        "es-ES": {"default": "es-ES-Neural2-A", "gender": "FEMALE"},
        "es-MX": {"default": "es-MX-Neural2-A", "gender": "FEMALE"},
        "fr": {"default": "fr-FR-Neural2-A", "gender": "FEMALE"},
        "fr-FR": {"default": "fr-FR-Neural2-A", "gender": "FEMALE"},
        "de": {"default": "de-DE-Neural2-A", "gender": "FEMALE"},
        "de-DE": {"default": "de-DE-Neural2-A", "gender": "FEMALE"},
        "ja": {"default": "ja-JP-Neural2-B", "gender": "FEMALE"},
        "ja-JP": {"default": "ja-JP-Neural2-B", "gender": "FEMALE"},
        "ko": {"default": "ko-KR-Neural2-A", "gender": "FEMALE"},
        "ko-KR": {"default": "ko-KR-Neural2-A", "gender": "FEMALE"},
        "zh": {"default": "cmn-CN-Neural2-A", "gender": "FEMALE"},
        "zh-CN": {"default": "cmn-CN-Neural2-A", "gender": "FEMALE"},
        "pt": {"default": "pt-BR-Neural2-A", "gender": "FEMALE"},
        "pt-BR": {"default": "pt-BR-Neural2-A", "gender": "FEMALE"},
        "it": {"default": "it-IT-Neural2-A", "gender": "FEMALE"},
        "it-IT": {"default": "it-IT-Neural2-A", "gender": "FEMALE"},
        "ru": {"default": "ru-RU-Neural2-A", "gender": "FEMALE"},
        "ru-RU": {"default": "ru-RU-Neural2-A", "gender": "FEMALE"},
        "ar": {"default": "ar-XA-Neural2-A", "gender": "FEMALE"},
        "hi": {"default": "hi-IN-Neural2-A", "gender": "FEMALE"},
    }

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        default_model: str = GOOGLE_TTS_MODEL_NEURAL2,
    ):
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )
        self.default_model = default_model
        self._client = None

    @property
    def client(self) -> texttospeech.TextToSpeechClient:
        """Lazy initialization of Google Cloud Text-to-Speech client."""
        if self._client is None:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = texttospeech.TextToSpeechClient(
                    credentials=credentials
                )
            else:
                self._client = texttospeech.TextToSpeechClient()
        return self._client

    def _resolve_voice(
        self,
        language_code: str,
        voice_name: Optional[str] = None,
        voice_gender: Optional[str] = None,
    ) -> Dict[str, str]:
        """Resolve voice configuration for a given language."""
        lang_info = self.LANGUAGE_VOICE_MAP.get(language_code, {})
        
        resolved_name = voice_name or lang_info.get("default", "en-US-Neural2-F")
        resolved_gender = voice_gender or lang_info.get("gender", "FEMALE")
        
        gender_enum = enums.SsmlVoiceGender.FEMALE
        if resolved_gender and "MALE" in resolved_gender.upper():
            gender_enum = enums.SsmlVoiceGender.MALE
        
        return {
            "name": resolved_name,
            "language_code": language_code,
            "ssml_gender": gender_enum,
        }

    def _resolve_audio_encoding(
        self, encoding_str: str
    ) -> enums.AudioEncoding:
        """Resolve audio encoding string to Google TTS enum."""
        encoding_map = {
            "MP3": enums.AudioEncoding.MP3,
            "LINEAR16": enums.AudioEncoding.LINEAR16,
            "OGG_OPUS": enums.AudioEncoding.OGG_OPUS,
            "MULAW": enums.AudioEncoding.MULAW,
            "ALAW": enums.AudioEncoding.ALAW,
        }
        return encoding_map.get(encoding_str.upper(), enums.AudioEncoding.MP3)

    def generate_audio(
        self,
        config: AudioPreviewConfig,
    ) -> AudioPreviewResult:
        """
        Generate spoken audio preview using Google Cloud Text-to-Speech API.
        
        Uses the Google Cloud Text-to-Speech API hosted at texttospeech.googleapis.com
        with Neural2 WaveNet models for natural-sounding speech synthesis.
        """
        voice_config = self._resolve_voice(
            language_code=config.language_code,
            voice_name=config.voice_name,
            voice_gender=config.voice_gender,
        )

        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_config["language_code"],
            name=voice_config["name"],
            ssml_gender=voice_config["ssml_gender"],
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=self._resolve_audio_encoding(config.audio_encoding),
            speaking_rate=config.speaking_rate,
            pitch=config.pitch,
            volume_gain_db=config.volume_gain_db,
            sample_rate_hertz=config.sample_rate_hertz,
        )

        synthesis_input = texttospeech.SynthesisInput(text=config.text)

        request = texttospeech.SynthesizeSpeechRequest(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
            model=config.model,
        )

        response = self.client.synthesize_speech(
            request=request,
            retry=retry.Retry(initial=0.5, maximum=30.0, multiplier=2.0),
        )

        audio_bytes = response.audio_content
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        duration_seconds = len(audio_bytes) / (config.sample_rate_hertz * 2)

        return AudioPreviewResult(
            audio_content=audio_bytes,
            audio_base64=audio_base64,
            language_code=config.language_code,
            voice_name=voice_config["name"],
            model=config.model,
            duration_seconds=duration_seconds,
            character_count=len(config.text),
            audio_format=config.audio_encoding.lower(),
        )

    def generate_batch_audio(
        self,
        texts: List[str],
        language_code: str,
        model: str = GOOGLE_TTS_MODEL_NEURAL2,
    ) -> List[AudioPreviewResult]:
        """Generate audio previews for multiple translated texts."""
        results = []
        for text in texts:
            config = AudioPreviewConfig(
                text=text,
                language_code=language_code,
                model=model,
            )
            result = self.generate_audio(config)
            results.append(result)
        return results


def generate_localized_audio_preview(
    translated_text: str,
    target_language: str,
    voice_name: str = None,
    model: str = GOOGLE_TTS_MODEL_NEURAL2,
    speaking_rate: float = 1.0,
) -> AudioPreviewResult:
    """
    Generate a spoken preview of translated copy using Google Cloud Text-to-Speech.
    
    Uses Google Cloud TTS API (texttospeech.googleapis.com) with Neural2 or WaveNet
    voice models to generate natural-sounding speech from translated text.
    
    Args:
        translated_text: The translated text to convert to speech
        target_language: Target language code (e.g., 'es', 'ja', 'fr')
        voice_name: Specific Google TTS voice name (optional)
        model: TTS model to use (Neural2, WaveNet, or Studio)
        speaking_rate: Speed of speech (0.25 to 4.0)
    
    Returns:
        AudioPreviewResult with audio content and metadata
    """
    generator = AudioPreviewGenerator(default_model=model)
    
    config = AudioPreviewConfig(
        text=translated_text,
        language_code=target_language,
        voice_name=voice_name,
        model=model,
        speaking_rate=speaking_rate,
    )
    
    return generator.generate_audio(config)


def generate_localized_audio_batch(
    translations: List[Dict[str, str]],
    model: str = GOOGLE_TTS_MODEL_NEURAL2,
) -> List[AudioPreviewResult]:
    """
    Generate spoken previews for a batch of translations.
    
    Each translation dict should have 'text' and 'language_code' keys.
    Uses Google Cloud Text-to-Speech (texttospeech.googleapis.com) for synthesis.
    """
    generator = AudioPreviewGenerator(default_model=model)
    results = []
    
    for item in translations:
        config = AudioPreviewConfig(
            text=item["text"],
            language_code=item["language_code"],
            model=model,
        )
        result = generator.generate_audio(config)
        results.append(result)
    
    return results


if __name__ == "__main__":
    samples = [
        {"text": "Bienvenido a nuestra aplicación", "language_code": "es"},
        {"text": "Bienvenue dans notre application", "language_code": "fr"},
        {"text": "Willkommen in unserer Anwendung", "language_code": "de"},
    ]
    
    results = generate_localized_audio_batch(samples)
    for result in results:
        print(f"  Voice: {result.voice_name}, Model: {result.model}")
        print(f"  Duration: {result.duration_seconds:.2f}s, Chars: {result.character_count}")
        print(f"  Audio size: {len(result.audio_content)} bytes")
        print()

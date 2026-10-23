"""
localized_audio_preview.py - Generate spoken previews of translated copy
using Google Cloud Text-to-Speech API v1 (SSML synthesis with WaveNet/
Neural2 voices).
"""

from typing import Optional, List
import base64
import os
from google.cloud import texttospeech
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SsmlVoiceGender,
    AudioEncoding,
)

from translation_client import GOOGLE_CLOUD_PROJECT, validate_client_ready
from translation_models import normalize_language_code

GOOGLE_TTS_API_ENDPOINT = "texttospeech.googleapis.com"
GOOGLE_CLOUD_TTS_MODEL = "neural2"
GOOGLE_CLOUD_TTS_MODEL_WAVENET = "wavenet"


def _get_language_voice_mapping(
    language_code: str,
    gender: Optional[SsmlVoiceGender] = None,
) -> VoiceSelectionParams:
    """
    Get Google Cloud TTS voice selection parameters for a given language.
    Uses Neural2 voices (Google's highest-quality models) when available.
    """
    lang = normalize_language_code(language_code)

    voice_map = {
        "en": {"voice": "en-US-Neural2-F", "gender": SsmlVoiceGender.FEMALE},
        "es": {"voice": "es-ES-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "fr": {"voice": "fr-FR-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "de": {"voice": "de-DE-Neural2-B", "gender": SsmlVoiceGender.MALE},
        "ja": {"voice": "ja-JP-Neural2-B", "gender": SsmlVoiceGender.MALE},
        "zh": {"voice": "cmn-CN-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "zh-CN": {"voice": "cmn-CN-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "ko": {"voice": "ko-KR-Neural2-B", "gender": SsmlVoiceGender.MALE},
        "pt": {"voice": "pt-BR-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "it": {"voice": "it-IT-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "ru": {"voice": "ru-RU-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "ar": {"voice": "ar-XA-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
        "hi": {"voice": "hi-IN-Neural2-A", "gender": SsmlVoiceGender.FEMALE},
    }

    config = voice_map.get(lang, {"voice": "en-US-Neural2-F", "gender": SsmlVoiceGender.FEMALE})

    voice_name = config["voice"]
    voice_gender = gender if gender is not None else config["gender"]

    return VoiceSelectionParams(
        language_code=lang,
        name=voice_name,
        ssml_gender=voice_gender,
    )


def generate_audio_preview(
    text: str,
    language_code: str = "en",
    gender: Optional[SsmlVoiceGender] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate a spoken audio preview of translated text using Google Cloud
    Text-to-Speech API v1 with Neural2 voice models.

    Args:
        text: The translated text to synthesize.
        language_code: BCP-47 language code for the target language.
        gender: Optional voice gender preference.
        speaking_rate: Speaking rate multiplier (0.25 to 4.0).
        pitch: Pitch adjustment in semitones (-20.0 to 20.0).
        output_path: Optional file path to save the audio file.

    Returns:
        Raw audio bytes (MP3 format).
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    client = texttospeech.TextToSpeechClient()

    voice = _get_language_voice_mapping(language_code, gender)

    synthesis_input = SynthesisInput(text=text)

    audio_config = AudioConfig(
        audio_encoding=AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_bytes = response.audio_content

    if output_path:
        with open(output_path, "wb") as out:
            out.write(audio_bytes)

    return audio_bytes


def generate_ssml_preview(
    text: str,
    language_code: str = "en",
    gender: Optional[SsmlVoiceGender] = None,
    emphasis: bool = False,
    pause_seconds: float = 0.0,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generate a spoken audio preview using Google Cloud Text-to-Speech API
    with SSML markup for enhanced control over pronunciation and pacing.

    Uses Google's Neural2 voice models for highest-quality synthesis.

    Args:
        text: Text content to synthesize with optional SSML wrapping.
        language_code: BCP-47 language code.
        gender: Optional voice gender preference.
        emphasis: Whether to wrap text in SSML emphasis tags.
        pause_seconds: Pause duration in seconds to add at the end.
        output_path: Optional file path to save the audio file.

    Returns:
        Raw audio bytes (MP3 format).
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    lang = normalize_language_code(language_code)
    voice = _get_language_voice_mapping(lang, gender)

    ssml_text = f'<speak><lang xml:lang="{lang}">'
    if emphasis:
        ssml_text += f"<emphasis level=\"moderate\">{text}</emphasis>"
    else:
        ssml_text += text
    if pause_seconds > 0:
        ssml_text += f'<break time="{int(pause_seconds * 1000)}ms"/>'
    ssml_text += "</lang></speak>"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = SynthesisInput(ssml=ssml_text)

    audio_config = AudioConfig(
        audio_encoding=AudioEncoding.MP3,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_bytes = response.audio_content

    if output_path:
        with open(output_path, "wb") as out:
            out.write(audio_bytes)

    return audio_bytes


def generate_batch_audio_previews(
    texts: List[str],
    language_code: str = "en",
    output_dir: Optional[str] = None,
    prefix: str = "preview",
) -> List[bytes]:
    """
    Generate spoken audio previews for multiple translated segments using
    Google Cloud Text-to-Speech API v1 with Neural2 voice models.

    Args:
        texts: List of translated text strings.
        language_code: Target language BCP-47 code.
        output_dir: Optional directory to save audio files.
        prefix: Filename prefix for saved audio files.

    Returns:
        List of audio byte arrays.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    all_audio: List[bytes] = []

    for idx, text in enumerate(texts):
        output_file = None
        if output_dir:
            output_file = os.path.join(output_dir, f"{prefix}_{idx:03d}.mp3")

        audio = generate_audio_preview(
            text=text,
            language_code=language_code,
            output_path=output_file,
        )
        all_audio.append(audio)

    return all_audio


if __name__ == "__main__":
    audio = generate_audio_preview(
        "Bonjour et bienvenue à notre service.",
        language_code="fr",
    )
    print(f"Generated audio preview: {len(audio)} bytes")

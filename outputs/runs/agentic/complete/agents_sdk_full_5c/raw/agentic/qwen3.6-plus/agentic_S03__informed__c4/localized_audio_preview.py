"""
Generate spoken previews of translated copy.

Provider: Amazon Polly Text-to-Speech
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses Amazon Polly to generate spoken audio previews of translated text.
Supports multiple voices and languages available through Polly's API,
including neural voices for more natural-sounding speech.

Models: Amazon Polly neural voices like 'Joanna', 'Matthew', 'Sophie',
'Aditi', 'Takumi', 'Zhiyu', and many more across 35+ languages.
"""

import base64
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


# Common Polly voice IDs organized by language
POLLY_VOICES = {
    "en-US": {
        "neural": ["Joanna", "Matthew", "Ruth", "Stephen", "Danielle", "Kevin"],
        "standard": ["Salli", "Kimberly", "Kendra", "Justin", "Ivy", "Joey"],
    },
    "en-GB": {
        "neural": ["Amy", "Arthur", "Emma", "Ryan"],
        "standard": ["Amy", "Brian", "Emma"],
    },
    "de-DE": {
        "neural": ["Vicki", "Daniel", "Katja", "Conrad"],
        "standard": ["Marlene", "Hans", "Vicki"],
    },
    "fr-FR": {
        "neural": ["Léa", "Rémi"],
        "standard": ["Céline", "Mathieu", "Léa"],
    },
    "es-ES": {
        "neural": ["Lucia", "Enrique"],
        "standard": ["Conchita", "Enrique"],
    },
    "ja-JP": {
        "neural": ["Kazuha", "Tomoko", "Takumi"],
        "standard": ["Mizuki", "Takumi"],
    },
    "zh-CN": {
        "neural": ["Zhiyu"],
        "standard": ["Zhiyu"],
    },
    "pt-BR": {
        "neural": ["Francisca", "Thiago"],
        "standard": ["Vitória", "Ricardo"],
    },
    "it-IT": {
        "neural": ["Bianca", "Adriano"],
        "standard": ["Carla", "Giorgio"],
    },
    "ko-KR": {
        "neural": ["Seoyeon"],
        "standard": ["Seoyeon"],
    },
}

DEFAULT_ENGINE = "neural"
DEFAULT_VOICE_FORMAT = "mp3"


def get_polly_client(
    region_name: str = "us-east-1",
) -> boto3.client:
    """
    Create an Amazon Polly client.

    Args:
        region_name: AWS region for the Polly service endpoint.

    Returns:
        Configured boto3 Polly client.
    """
    return boto3.client(
        "polly",
        region_name=region_name,
    )


def generate_audio_preview(
    text: str,
    language_code: str = "en-US",
    *,
    voice_id: Optional[str] = None,
    engine: str = DEFAULT_ENGINE,
    output_format: str = DEFAULT_VOICE_FORMAT,
    sample_rate: Optional[str] = None,
    speed: Optional[str] = None,
    polly_client: Optional[boto3.client] = None,
) -> bytes:
    """
    Generate a spoken audio preview of translated text using Amazon Polly.

    Args:
        text: The text to synthesize into speech.
        language_code: Language/region code (e.g., 'en-US', 'de-DE', 'fr-FR').
        voice_id: Specific Polly voice ID. If None, a default voice for the
            language and engine type is selected.
        engine: Voice engine type. 'neural' for neural TTS, 'standard' for
            standard TTS. Neural voices sound more natural.
        output_format: Audio format ('mp3', 'ogg_vorbis', 'pcm').
        sample_rate: Sample rate for PCM output (e.g., '8000', '16000',
            '22050', '24000'). Not applicable for MP3.
        speed: SSML speed adjustment (e.g., '80%', '120%').
        polly_client: Optional pre-created Polly client.

    Returns:
        Raw audio bytes in the requested format.

    Raises:
        ValueError: If the voice or engine is not available for the language.
        ClientError: If the Polly API request fails.
    """
    if polly_client is None:
        polly_client = get_polly_client()

    if not text or not text.strip():
        return b""

    # Resolve voice ID
    resolved_voice = voice_id
    if resolved_voice is None:
        voices = POLLY_VOICES.get(language_code, {})
        engine_voices = voices.get(engine, [])
        if engine_voices:
            resolved_voice = engine_voices[0]
        else:
            # Fall back to standard if neural not available
            standard_voices = voices.get("standard", [])
            if standard_voices:
                resolved_voice = standard_voices[0]
            else:
                resolved_voice = "Joanna"  # default fallback
                engine = "standard"

    # Build synthesis kwargs
    synthesize_kwargs = {
        "Text": text,
        "VoiceId": resolved_voice,
        "OutputFormat": output_format,
        "Engine": engine,
    }

    if sample_rate and output_format == "pcm":
        synthesize_kwargs["SampleRate"] = sample_rate

    response = polly_client.synthesize_speech(**synthesize_kwargs)

    audio_bytes = response["AudioStream"].read()

    # Apply speed adjustment if requested (via SSML)
    if speed and speed != "100%":
        ssml_text = (
            f'<speak><prosody speed="{speed}">{text}</prosody></speak>'
        )
        response = polly_client.synthesize_speech(
            Text=ssml_text,
            VoiceId=resolved_voice,
            OutputFormat=output_format,
            Engine=engine,
        )
        audio_bytes = response["AudioStream"].read()

    return audio_bytes


def generate_audio_preview_base64(
    text: str,
    language_code: str = "en-US",
    *,
    voice_id: Optional[str] = None,
    engine: str = DEFAULT_ENGINE,
    output_format: str = DEFAULT_VOICE_FORMAT,
    polly_client: Optional[boto3.client] = None,
) -> str:
    """
    Generate audio preview and return as base64-encoded string.

    Useful for embedding audio in web applications or APIs.

    Args:
        text: The text to synthesize.
        language_code: Language/region code.
        voice_id: Specific Polly voice ID.
        engine: Voice engine type.
        output_format: Audio format.
        polly_client: Optional pre-created Polly client.

    Returns:
        Base64-encoded audio string.
    """
    audio_bytes = generate_audio_preview(
        text=text,
        language_code=language_code,
        voice_id=voice_id,
        engine=engine,
        output_format=output_format,
        polly_client=polly_client,
    )
    return base64.b64encode(audio_bytes).decode("utf-8")


def batch_generate_audio_previews(
    text_items: list[tuple[str, str]],
    *,
    engine: str = DEFAULT_ENGINE,
    output_format: str = DEFAULT_VOICE_FORMAT,
    polly_client: Optional[boto3.client] = None,
) -> list[tuple[str, bytes]]:
    """
    Generate audio previews for multiple text/language pairs.

    Args:
        text_items: List of (text, language_code) tuples.
        engine: Voice engine type.
        output_format: Audio format.
        polly_client: Optional pre-created Polly client.

    Returns:
        List of (language_code, audio_bytes) tuples.
    """
    if polly_client is None:
        polly_client = get_polly_client()

    results = []
    for text, lang_code in text_items:
        audio = generate_audio_preview(
            text=text,
            language_code=lang_code,
            engine=engine,
            output_format=output_format,
            polly_client=polly_client,
        )
        results.append((lang_code, audio))

    return results


def list_available_voices(
    language_code: Optional[str] = None,
    *,
    polly_client: Optional[boto3.client] = None,
) -> list[dict]:
    """
    List available Polly voices, optionally filtered by language.

    Args:
        language_code: Optional language code filter (e.g., 'en-US').
        polly_client: Optional pre-created Polly client.

    Returns:
        List of voice info dicts with VoiceId, LanguageCode, etc.
    """
    if polly_client is None:
        polly_client = get_polly_client()

    kwargs: dict = {}
    if language_code:
        kwargs["LanguageCode"] = language_code

    response = polly_client.describe_voices(**kwargs)
    return response.get("Voices", [])


if __name__ == "__main__":
    audio = generate_audio_preview(
        text="Hello, this is a translation preview.",
        language_code="en-US",
        voice_id="Joanna",
    )
    print(f"Generated audio: {len(audio)} bytes")
    print(f"Base64 preview: {base64.b64encode(audio).decode('utf-8')[:80]}...")

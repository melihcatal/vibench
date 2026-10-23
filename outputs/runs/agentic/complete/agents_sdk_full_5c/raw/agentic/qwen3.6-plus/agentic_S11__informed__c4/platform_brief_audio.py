"""Generate spoken briefings from platform outputs.

Uses Amazon Polly Text-to-Speech API to synthesize spoken audio briefings
from platform model text outputs. Supports multiple voices, languages, and
output formats for creating accessible audio summaries.

Provider: Amazon Polly
SDK: boto3 (polly client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import io
from typing import Any, Dict, Optional

from model_client import create_polly_client, resolve_bedrock_credentials
from model_models import AudioResult, build_polly_payload


POLLY_VOICES = {
    "en-US": ["Joanna", "Matthew", "Salli", "Ivy", "Kendra", "Kimberly"],
    "en-GB": ["Amy", "Emma", "Brian", "Arthur"],
    "es-ES": ["Lucia", "Conchita", "Enrique"],
    "es-US": ["Lupe", "Miguel"],
    "fr-FR": ["Celine", "Mathieu", "Lea"],
    "de-DE": ["Marlene", "Hans", "Vicki"],
    "it-IT": ["Carla", "Giorgio"],
    "ja-JP": ["Mizuki", "Takumi"],
    "pt-BR": ["Vitoria", "Ricardo"],
    "zh-CN": ["Zhiyu"],
}


def generate_audio_briefing(
    text: str,
    voice_id: str = "Joanna",
    output_format: str = "mp3",
    sample_rate: str = "22050",
    engine: str = "neural",
    speech_rate: Optional[str] = None,
    volume: Optional[str] = None,
) -> AudioResult:
    """Generate a spoken audio briefing from platform model output.

    Uses Amazon Polly to synthesize speech from text, creating an audio
    briefing suitable for playback or distribution.

    Args:
        text: Text content to synthesize as speech.
        voice_id: Polly voice identifier.
        output_format: Audio output format ('mp3', 'ogg_vorbis', 'pcm').
        sample_rate: Sample rate in Hz (8000, 16000, 22050, 24000).
        engine: Synthesis engine ('standard', 'neural', 'long-form').
        speech_rate: Optional SSML speech rate adjustment.
        volume: Optional SSML volume adjustment.

    Returns:
        AudioResult with audio data and metadata.

    Raises:
        ValueError: If text is empty or exceeds length limits.
        Exception: If Polly API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Text to synthesize cannot be empty")

    if len(text) > 3000:
        raise ValueError(
            "Text exceeds Amazon Polly 3000 character limit for single request. "
            "Use SSML or chunk longer texts."
        )

    speak_text = text
    if speech_rate or volume:
        rate_attr = f' rate="{speech_rate}"' if speech_rate else ""
        volume_attr = f' volume="{volume}"' if volume else ""
        speak_text = (
            f'<speak><prosper{rate_attr}{volume_attr}>{text}</prosper></speak>'
        )

    credentials = resolve_bedrock_credentials()
    client = create_polly_client(credentials)

    kwargs = {
        "Text": speak_text,
        "VoiceId": voice_id,
        "OutputFormat": output_format,
        "Engine": engine,
    }

    if output_format != "mp3":
        kwargs["SampleRate"] = sample_rate

    response = client.synthesize_speech(**kwargs)

    audio_stream = response.get("AudioStream")
    if audio_stream is None:
        raise ValueError("Polly returned empty audio stream")

    audio_data = audio_stream.read()

    content_type_map = {
        "mp3": "audio/mpeg",
        "ogg_vorbis": "audio/ogg",
        "pcm": "audio/pcm",
    }

    return AudioResult(
        audio_data=audio_data,
        content_type=content_type_map.get(output_format, f"audio/{output_format}"),
        sample_rate=int(sample_rate),
        metadata={
            "provider": "Amazon Polly",
            "service": "polly",
            "voice_id": voice_id,
            "engine": engine,
            "output_format": output_format,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
            "text_length": len(text),
            "audio_size_bytes": len(audio_data),
        },
    )


def generate_briefing_with_ssml(
    text: str,
    voice_id: str = "Joanna",
    include_greeting: bool = True,
    include_signoff: bool = True,
) -> AudioResult:
    """Generate audio briefing with SSML formatting for professional delivery.

    Args:
        text: Core briefing content.
        voice_id: Polly voice identifier.
        include_greeting: Add introductory greeting.
        include_signoff: Add closing signoff.

    Returns:
        AudioResult with formatted audio.
    """
    ssml_parts = ['<speak>']

    if include_greeting:
        ssml_parts.append('<break time="200ms"/>')
        ssml_parts.append('Here is your briefing.<break time="300ms"/>')

    ssml_parts.append('<break time="200ms"/>')
    ssml_parts.append(f'<p>{text}</p>')

    if include_signoff:
        ssml_parts.append('<break time="400ms"/>')
        ssml_parts.append('End of briefing.')

    ssml_parts.append('</speak>')

    ssml_text = " ".join(ssml_parts)

    return generate_audio_briefing(
        text=ssml_text,
        voice_id=voice_id,
    )


def get_available_voices(language_code: Optional[str] = None) -> Dict[str, list]:
    """Get available Polly voices, optionally filtered by language.

    Args:
        language_code: Optional language code filter.

    Returns:
        Dict mapping language codes to lists of voice IDs.
    """
    if language_code:
        return {language_code: POLLY_VOICES.get(language_code, [])}
    return dict(POLLY_VOICES)


def save_audio_to_file(audio_result: AudioResult, filepath: str) -> str:
    """Save audio result to a file.

    Args:
        audio_result: AudioResult from generate_audio_briefing.
        filepath: Output file path.

    Returns:
        The filepath where audio was saved.
    """
    with open(filepath, "wb") as f:
        f.write(audio_result.audio_data)
    return filepath


if __name__ == "__main__":
    text = "Welcome to today's briefing. Machine learning continues to advance rapidly."
    result = generate_audio_briefing(text, voice_id="Joanna")
    print(f"Audio generated: {result.metadata['audio_size_bytes']} bytes")
    print(f"Format: {result.content_type}")

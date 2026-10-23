"""
Local request, response, and normalization helpers for Amazon Polly Text-to-Speech.

Defines data models for synthesis requests, voice selection, and audio responses
with provider-specific normalization for Amazon Polly.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

# Amazon Polly specific constants
POLLY_VOICES = {
    "en-US": ["Joanna", "Matthew", "Salli", "Kimberly", "Justin"],
    "en-GB": ["Amy", "Brian", "Emma", "Arthur"],
    "es-ES": ["Lucia", "Enrique", "Conchita"],
    "es-US": ["Penelope", "Miguel", "Lupe"],
    "fr-FR": ["Lea", "Mathieu", "Celine"],
    "de-DE": ["Vicki", "Hans", "Marlene"],
    "it-IT": ["Carla", "Giorgio", "Bianca"],
    "pt-BR": ["Vitoria", "Ricardo"],
    "ja-JP": ["Mizuki", "Takumi"],
    "ko-KR": ["Seoyeon"],
}


class OutputFormat(str, Enum):
    """Amazon Polly supported audio output formats."""
    MP3 = "mp3"
    OGG_VORBIS = "ogg_vorbis"
    PCM = "pcm"


class TextType(str, Enum):
    """Amazon Polly text input types."""
    TEXT = "text"
    SSML = "ssml"


@dataclass
class SynthesisRequest:
    """Request model for Amazon Polly synthesis."""
    text: str
    voice_id: str = "Joanna"
    output_format: OutputFormat = OutputFormat.MP3
    text_type: TextType = TextType.TEXT
    language_code: Optional[str] = None
    sample_rate: Optional[str] = None
    
    def to_polly_kwargs(self) -> dict:
        """Convert to Amazon Polly synthesize_speech kwargs."""
        kwargs = {
            "Text": self.text,
            "VoiceId": self.voice_id,
            "OutputFormat": self.output_format.value,
            "TextType": self.text_type.value,
        }
        if self.language_code:
            kwargs["LanguageCode"] = self.language_code
        return kwargs


@dataclass
class SSMLSynthesisRequest(SynthesisRequest):
    """Request model for SSML-based synthesis with prosody controls."""
    voice_id: str = "Joanna"
    text_type: TextType = TextType.SSML
    prosody_rate: Optional[str] = None
    prosody_pitch: Optional[str] = None
    prosody_volume: Optional[str] = None
    
    def wrap_with_ssml(self, text: str) -> str:
        """Wrap text in Amazon Polly compatible SSML."""
        ssml_parts = ['<speak>']
        
        if self.prosody_rate or self.prosody_pitch or self.prosody_volume:
            prosody_attrs = []
            if self.prosody_rate:
                prosody_attrs.append(f'rate="{self.prosody_rate}"')
            if self.prosody_pitch:
                prosody_attrs.append(f'pitch="{self.prosody_pitch}"')
            if self.prosody_volume:
                prosody_attrs.append(f'volume="{self.prosody_volume}"')
            prosody_tag = f'<prosody {" ".join(prosody_attrs)}>'
            ssml_parts.append(prosody_tag)
            ssml_parts.append(text)
            ssml_parts.append('</prosody>')
        else:
            ssml_parts.append(text)
            
        ssml_parts.append('</speak>')
        return "".join(ssml_parts)


@dataclass
class VoiceInfo:
    """Normalized voice metadata from Amazon Polly."""
    voice_id: str
    name: str
    language_code: str
    language_name: str
    gender: str
    supported_engines: List[str] = field(default_factory=list)
    
    @classmethod
    def from_polly_response(cls, voice_data: dict) -> "VoiceInfo":
        """Create VoiceInfo from Amazon Polly describe_voices response item."""
        return cls(
            voice_id=voice_data["Id"],
            name=voice_data.get("Name", voice_data["Id"]),
            language_code=voice_data["LanguageCode"],
            language_name=voice_data.get("LanguageName", ""),
            gender=voice_data.get("Gender", "Unknown"),
            supported_engines=voice_data.get("SupportedEngines", []),
        )


@dataclass
class SynthesisResponse:
    """Response model for synthesis operation."""
    audio_stream: bytes
    content_type: str
    request_id: str
    voice_id: str
    output_format: str
    characters_used: int = 0
    
    @classmethod
    def from_polly_response(cls, response: dict, voice_id: str) -> "SynthesisResponse":
        """Create SynthesisResponse from Amazon Polly synthesize_speech response."""
        audio_stream = response["AudioStream"].read()
        return cls(
            audio_stream=audio_stream,
            content_type=response.get("ContentType", "audio/mpeg"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
            voice_id=voice_id,
            output_format=response.get("OutputFormat", "mp3"),
            characters_used=response.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amzn-request-charged", "0"),
        )


def normalize_voice_id(voice_id: str, locale: str = "en-US") -> str:
    """
    Normalize or validate a voice ID for Amazon Polly.
    
    If voice_id is not in Polly's known voices for the locale,
    return the default voice for that locale.
    """
    valid_voices = POLLY_VOICES.get(locale, [])
    if voice_id in valid_voices or voice_id in [v for voices in POLLY_VOICES.values() for v in voices]:
        return voice_id
    # Return default for locale
    if valid_voices:
        return valid_voices[0]
    return "Joanna"


def build_ssml(
    text: str,
    voice_name: Optional[str] = None,
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
    volume: Optional[str] = None,
    emphasis_level: Optional[str] = None,
    break_duration: Optional[str] = None,
) -> str:
    """
    Build Amazon Polly compatible SSML string.
    
    Args:
        text: The text content to wrap
        voice_name: Optional amazon:voice tag
        rate: Speaking rate (e.g., 'slow', 'fast', '150%')
        pitch: Pitch adjustment (e.g., '+10%', '-1st')
        volume: Volume level (e.g., 'loud', 'soft', '-6dB')
        emphasis_level: Emphasis strength ('strong', 'moderate', 'reduced')
        break_duration: Pause duration (e.g., '500ms', '1s')
    """
    parts = ['<speak>']
    
    if voice_name:
        parts.append(f'<amazon:domain name="conversational">')
    
    if emphasis_level:
        parts.append(f'<emphasis level="{emphasis_level}">')
        
    if rate or pitch or volume:
        attrs = []
        if rate:
            attrs.append(f'rate="{rate}"')
        if pitch:
            attrs.append(f'pitch="{pitch}"')
        if volume:
            attrs.append(f'volume="{volume}"')
        parts.append(f'<prosody {" ".join(attrs)}>')
    
    parts.append(text)
    
    if rate or pitch or volume:
        parts.append('</prosody>')
        
    if emphasis_level:
        parts.append('</emphasis>')
        
    if break_duration:
        parts.append(f'<break time="{break_duration}"/>')
    
    if voice_name:
        parts.append('</amazon:domain>')
    
    parts.append('</speak>')
    return "".join(parts)

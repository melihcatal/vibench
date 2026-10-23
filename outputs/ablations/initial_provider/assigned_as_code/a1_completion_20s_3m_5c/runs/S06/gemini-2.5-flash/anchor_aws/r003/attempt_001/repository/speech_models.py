from typing import Literal, Optional
from pydantic import BaseModel, Field

class SynthesizeTextInput(BaseModel):
    text: str
    voice_id: str = Field(default="Joanna", description="Voice ID for synthesis.")
    output_format: Literal["mp3", "ogg_vorbis", "pcm"] = Field(default="mp3", description="Output audio format.")

class SynthesizeSsmlInput(BaseModel):
    ssml: str
    voice_id: str = Field(default="Joanna", description="Voice ID for synthesis.")
    output_format: Literal["mp3", "ogg_vorbis", "pcm"] = Field(default="mp3", description="Output audio format.")

class VoiceSelectionInput(BaseModel):
    language_code: Optional[str] = Field(None, description="Language code to filter voices.")
    gender: Optional[Literal["Male", "Female"]] = Field(None, description="Gender to filter voices.")

class AudioOutput(BaseModel):
    audio_bytes: bytes
    content_type: str

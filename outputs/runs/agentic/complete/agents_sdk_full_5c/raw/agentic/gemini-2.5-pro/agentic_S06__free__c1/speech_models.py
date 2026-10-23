from typing import Optional, List
from pydantic import BaseModel, Field

class VoiceSelectionParams(BaseModel):
    language_code: str = Field(..., description="The IETF language tag of the voice to use.")
    name: Optional[str] = Field(None, description="The specific name of the voice.")
    ssml_gender: Optional[str] = Field(None, description="The preferred gender of the voice. (e.g., 'FEMALE', 'MALE')")

class SynthesisRequest(BaseModel):
    text: str
    voice_params: VoiceSelectionParams
    speaking_rate: float = 1.0
    pitch: float = 0.0
    
class SynthesisSSMLRequest(BaseModel):
    ssml: str
    voice_params: VoiceSelectionParams
    speaking_rate: float = 1.0
    pitch: float = 0.0

class Voice(BaseModel):
    name: str
    language_codes: List[str]
    ssml_gender: str
    natural_sample_rate_hertz: int

    @staticmethod
    def from_google_voice(voice_obj):
        return Voice(
            name=voice_obj.name,
            language_codes=list(voice_obj.language_codes),
            ssml_gender=voice_obj.ssml_gender.name,
            natural_sample_rate_hertz=voice_obj.natural_sample_rate_hertz
        )

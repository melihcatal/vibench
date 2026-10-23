from google.cloud import texttospeech
from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str | None = None
    ssml: str | None = None
    language_code: str = "en-US"
    ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.LINEAR16

def create_synthesis_input(request: SynthesisRequest) -> texttospeech.SynthesisInput:
    if request.text:
        return texttospeech.SynthesisInput(text=request.text)
    elif request.ssml:
        return texttospeech.SynthesisInput(ssml=request.ssml)
    else:
        raise ValueError("Either 'text' or 'ssml' must be provided in SynthesisRequest.")

def create_voice_params(request: SynthesisRequest) -> texttospeech.VoiceSelectionParams:
    return texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        ssml_gender=request.ssml_gender
    )

def create_audio_config(request: SynthesisRequest) -> texttospeech.AudioConfig:
    return texttospeech.AudioConfig(
        audio_encoding=request.audio_encoding
    )

def extract_audio_content(response: texttospeech.SynthesizeSpeechResponse) -> bytes:
    return response.audio_content

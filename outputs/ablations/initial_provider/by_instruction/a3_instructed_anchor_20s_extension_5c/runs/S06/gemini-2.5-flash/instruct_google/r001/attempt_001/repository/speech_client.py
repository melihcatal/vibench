import os
from google.cloud import texttospeech
from speech_models import (
    SynthesizeSpeechRequest,
    SynthesizeSpeechResponse,
    VoiceSelectionParams,
    AudioConfig,
    SynthesisInput,
    Voice,
    ListVoicesResponse
)

class TextToSpeechClient:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(
        self, request: SynthesizeSpeechRequest
    ) -> SynthesizeSpeechResponse:
        synthesis_input = None
        if request.input.text:
            synthesis_input = texttospeech.SynthesisInput(text=request.input.text)
        elif request.input.ssml:
            synthesis_input = texttospeech.SynthesisInput(ssml=request.input.ssml)

        voice = texttospeech.VoiceSelectionParams(
            language_code=request.voice.language_code,
            name=request.voice.name,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, request.voice.ssml_gender)
            if request.voice.ssml_gender else None,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_config.audio_encoding),
            speaking_rate=request.audio_config.speaking_rate,
            pitch=request.audio_config.pitch,
            volume_gain_db=request.audio_config.volume_gain_db,
            sample_rate_hertz=request.audio_config.sample_rate_hertz,
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return SynthesizeSpeechResponse(audio_content=response.audio_content)

    def list_voices(self, language_code: Optional[str] = None) -> ListVoicesResponse:
        response = self.client.list_voices(language_code=language_code)
        voices = []
        for voice in response.voices:
            voices.append(Voice(
                name=voice.name,
                supported_language_codes=list(voice.supported_language_codes),
                ssml_gender=voice.ssml_gender.name,
                natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
            ))
        return ListVoicesResponse(voices=voices)

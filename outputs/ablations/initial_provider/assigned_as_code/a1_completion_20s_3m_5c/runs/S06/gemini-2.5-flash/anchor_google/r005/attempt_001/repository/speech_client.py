from google.cloud import texttospeech
from speech_models import SynthesisRequest, SynthesisResponse, Voice, VoiceSelection


class TextToSpeechClient:
    def __init__(self):
        self._client = texttospeech.TextToSpeechClient()

    def synthesize(self, request: SynthesisRequest) -> SynthesisResponse:
        synthesis_input = None
        if request.text:
            synthesis_input = texttospeech.SynthesisInput(text=request.text)
        elif request.ssml:
            synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)
        else:
            raise ValueError("Either 'text' or 'ssml' must be provided in the request.")

        voice_params = texttospeech.VoiceSelectionParams(
            language_code=request.language_code,
            name=request.voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding[request.audio_encoding]
        )

        response = self._client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config
        )

        return SynthesisResponse(
            audio_bytes=response.audio_content,
            content_type=f"audio/{request.audio_encoding.lower()}"
        )

    def list_voices(self, language_code: Optional[str] = None) -> list[Voice]:
        response = self._client.list_voices(language_code=language_code)
        voices = []
        for voice in response.voices:
            voices.append(
                Voice(
                    name=voice.name,
                    language_codes=list(voice.language_codes),
                    gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
                )
            )
        return voices

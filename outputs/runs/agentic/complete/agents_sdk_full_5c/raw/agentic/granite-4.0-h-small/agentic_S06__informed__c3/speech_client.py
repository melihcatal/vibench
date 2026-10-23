import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, AudioDataStream, SpeechSynthesizer

class AzureSpeechClient:
    """Thin wrapper around Azure Speech TTS SDK."""
    def __init__(self):
        self.speech_config = SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION")
        )
        self.synthesizer = SpeechSynthesizer(speech_config=self.speech_config)

    def synthesize_speech(
        self,
        text: str,
        voice_name: str,
        voice_config: dict,
        ssml: bool = False,
        output_format = "wav"
    ) -> AudioDataStream:
        """Synthesize text (or SSML) to an AudioDataStream.
        voice_config must contain locale, gender, style if needed.
        """
        if ssml:
            result = self.synthesizer.speak_ssml(text, voice_name=voice_name, voice_config=voice_config)
        else:
            result = self.synthesizer.speak_text_async(text, voice_name=voice_name, voice_config=voice_config).get()
        return AudioDataStream(result.audio_data)

    def list_voices(self, language_code: str = None) -> list:
        """List voices that match the optional language_code.
        Returns a list of VoiceInfo objects (name, locale, gender, language)."""
        voices = self.speech_config.get_voices_list(language=language_code)
        return [v for v in voices]

    def shutdown(self):
        pass  # Clean up resources if needed

def get_text_to_speech_client() -> AzureSpeechClient:
    """Utility to provide a singleton client instance."""
    _client = getattr(get_text_to_speech_client, "_instance", None)
    if _client is None:
        _client = AzureSpeechClient()
        setattr(get_text_to_speech_client, "_instance", _client)
    return _client

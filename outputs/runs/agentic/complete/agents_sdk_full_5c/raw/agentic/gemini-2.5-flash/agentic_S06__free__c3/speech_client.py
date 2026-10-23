from google.cloud import texttospeech

class TextToSpeechClientHelper:
    """Provides local configuration and client helper utilities for Google Cloud Text-to-Speech."""

    def __init__(self):
        """Initializes the Google Cloud Text-to-Speech client."""
        self._client = texttospeech.TextToSpeechClient()

    def get_client(self) -> texttospeech.TextToSpeechClient:
        """Returns the initialized TextToSpeechClient."""
        return self._client

    @staticmethod
    def get_audio_config(audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> texttospeech.AudioConfig:
        """Returns a default audio configuration."""
        return texttospeech.AudioConfig(audio_encoding=audio_encoding)

    @staticmethod
    def get_voice_selection_params(language_code: str = "en-US", ssml_gender: str = "NEUTRAL", name: str = None) -> texttospeech.VoiceSelectionParams:
        """Returns voice selection parameters."""
        gender_enum = getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper())
        return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=gender_enum,
            name=name
        )

if __name__ == '__main__':
    # Example usage
    # helper = TextToSpeechClientHelper()
    # client = helper.get_client()
    # print(f"TextToSpeechClient instance created: {client}")
    #
    # voice_params = helper.get_voice_selection_params(language_code="en-US", ssml_gender="FEMALE")
    # print(f"Example voice params: {voice_params}")
    pass

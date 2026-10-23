from google.cloud import texttospeech

# Use environment variable for authentication
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

class TextToSpeechClient:
    def __init__(self):
        # Create a client instance; credentials are auto-loaded
        self.tts_client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, input_, voice, audio_config):
        return self.tts_client.synthesize_speech(input=input_, voice=voice, audio_config=audio_config)

    def list_voices(self, language_code=None):
        return self.tts_client.list_voices(language_code=language_code)

    def select_voice(self, voice_name=None):
        # If a voice name is provided, return a VoiceSelectionParams
        if voice_name:
            return texttospeech.VoiceSelectionParams(name=voice_name)
        # Otherwise default to a neutral voice (Google's default)
        return texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-D")

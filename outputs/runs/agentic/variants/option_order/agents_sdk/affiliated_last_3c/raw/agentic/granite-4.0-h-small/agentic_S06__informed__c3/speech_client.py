# Azure AI Speech SDK integration (azur espeech service)
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastus')

def init_config():
    if not AZURE_SPEECH_KEY:
        raise EnvironmentError('Set AZURE_SPEECH_KEY environment variable')
    config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    return config

class TextToSpeechClient:
    def __init__(self):
        self.speech_config = init_config()
        self.synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=AudioConfig())

    def synthesize_speech(self, text, voice_name=None, ssml=False, format='riff-16khz-16bit-mono-pcm'):
        # prepare payload
        if ssml:
            text_input = text
        else:
            text_input = f'<speak version=\"1.0\" xml:lang=\"en-US\"><voice name=\"{voice_name or self.speech_config.voice_name}\">{text}</voice></speak>'
        result = self.synthesizer.speak_text_async(text_input).get()
        if result.reason != result.reason.Success:
            raise RuntimeError(f"Synthesis error: {result.reason}")
        return result.audio_data

    def list_voices(self):
        voices = self.speech_config.get_voices_async().get()
        return [voice for voice in voices]

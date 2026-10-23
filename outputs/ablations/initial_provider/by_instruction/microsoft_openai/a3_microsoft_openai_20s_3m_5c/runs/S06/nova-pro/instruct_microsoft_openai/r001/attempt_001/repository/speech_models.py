from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

class SpeechRequest:
    def __init__(self, text: str, voice_name: str = None, output_format: SpeechSynthesisOutputFormat = SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3):
        self.text = text
        self.voice_name = voice_name
        self.output_format = output_format

class SpeechResponse:
    def __init__(self, audio_data: bytes):
        self.audio_data = audio_data
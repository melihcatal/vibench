from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

class SpeechModel:
    def __init__(self, text, format=SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3):
        self.text = text
        self.format = format
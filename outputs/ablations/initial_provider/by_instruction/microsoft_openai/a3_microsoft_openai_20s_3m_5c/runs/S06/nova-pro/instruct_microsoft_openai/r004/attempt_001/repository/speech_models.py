from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

def get_default_synthesis_format() -> SpeechSynthesisOutputFormat:
    return SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
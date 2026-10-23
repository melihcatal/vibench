from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

def get_synthesis_output_format():
    return SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
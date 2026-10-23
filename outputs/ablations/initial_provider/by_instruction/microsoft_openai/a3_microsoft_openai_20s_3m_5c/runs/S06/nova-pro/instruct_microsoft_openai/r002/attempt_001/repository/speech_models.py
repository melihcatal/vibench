from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

def get_default_synthesis_output_format():
    return SpeechSynthesisOutputFormat.Raw16Khz16BitMonoPcm
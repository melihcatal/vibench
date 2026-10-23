from azure.cognitiveservices.speech import SpeechSynthesisResult, ResultReason

def normalize_result(result):
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None
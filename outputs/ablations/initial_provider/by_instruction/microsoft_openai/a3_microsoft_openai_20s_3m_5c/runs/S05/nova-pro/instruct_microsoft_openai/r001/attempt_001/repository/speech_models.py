import azure.cognitiveservices.speech as speechsdk

def normalize_recognition_result(result):
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    return None
import azure.cognitiveservices.speech as speechsdk

def normalize_result(result):
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Speech could not be recognized."
    else:
        return "Error encountered: " + result.reason
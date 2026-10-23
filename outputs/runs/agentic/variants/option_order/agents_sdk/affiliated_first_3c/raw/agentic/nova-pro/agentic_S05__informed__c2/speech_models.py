class SpeechModels:
    @staticmethod
    def normalize_result(result):
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized"
        else:
            return "Error encountered"

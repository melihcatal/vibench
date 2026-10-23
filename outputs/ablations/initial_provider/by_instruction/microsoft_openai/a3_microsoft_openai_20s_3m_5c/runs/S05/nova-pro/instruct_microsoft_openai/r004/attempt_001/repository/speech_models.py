from azure.cognitiveservices.speech import SpeechRecognitionResult, SpeechRecognitionCanceled

def normalize_recognition_result(result):
    if isinstance(result, SpeechRecognitionResult):
        return result.text
    elif isinstance(result, SpeechRecognitionCanceled):
        return 'Canceled: {}'.format(result.cancellation_details.error_details)
    else:
        return 'Unknown result type'
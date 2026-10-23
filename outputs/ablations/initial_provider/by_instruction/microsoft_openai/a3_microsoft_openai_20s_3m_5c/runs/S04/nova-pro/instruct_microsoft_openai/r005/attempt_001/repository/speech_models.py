def normalize_transcription_result(result):
    if result and result.reason == ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None
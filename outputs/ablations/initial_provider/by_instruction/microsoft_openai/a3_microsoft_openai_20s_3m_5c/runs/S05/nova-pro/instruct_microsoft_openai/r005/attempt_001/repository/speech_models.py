def normalize_result(result):
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == ResultReason.NoMatch:
        return 'No match: {}'.format(result.no_match_details)
    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return 'Canceled: {}'.format(cancellation_details)
import azure.cognitiveservices.speech as speechsdk

def handle_partial_results(result):
    if result.reason == speechsdk.ResultReason.RecognizingSpeech:
        print('PARTIAL: Text={}'.format(result.text))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('FINAL: Text={}'.format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print('NOMATCH: Speech could not be recognized.')
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print('CANCELED: Reason={}'.format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print('CANCELED: ErrorCode={}'.format(cancellation_details.error_code))
            print('CANCELED: ErrorDetails={}'.format(cancellation_details.error_details))
            print('CANCELED: Did you update the subscription info?')

if __name__ == '__main__':
    pass  # This file is intended to be imported and used in other files.
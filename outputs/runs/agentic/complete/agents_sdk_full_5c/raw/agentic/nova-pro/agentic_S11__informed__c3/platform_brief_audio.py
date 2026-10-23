import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription='YOUR_AZURE_SPEECH_KEY', region='YOUR_AZURE_SPEECH_REGION')
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('Speech synthesized for text [{}]'.format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print('Speech synthesis canceled: {}'.format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print('Error details: {}'.format(cancellation_details.error_details))
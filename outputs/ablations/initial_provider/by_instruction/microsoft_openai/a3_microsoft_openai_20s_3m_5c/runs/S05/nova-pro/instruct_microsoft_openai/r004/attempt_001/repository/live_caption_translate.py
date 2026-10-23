import azure.cognitiveservices.speech as speechsdk

def translate_caption(caption, target_language='es'):
    speech_config = speechsdk.SpeechConfig(subscription="YourSubscriptionKey", region="YourServiceRegion")
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, language=target_language)
    result = speech_synthesizer.speak_text_async(caption).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        print('Speech synthesis canceled: {}'.format(result.cancellation_details.reason))
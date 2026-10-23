import azure.cognitiveservices.speech as speechsdk

def translate_caption(caption, target_language):
    speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
    speech_config.speech_synthesis_voice_name = 'en-US-AriaNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, language=target_language)
    result = speech_synthesizer.speak_text_async(caption).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        print('Speech synthesis canceled: {}'.format(result.cancellation_details.reason))
        return None

if __name__ == '__main__':
    pass  # This file is intended to be imported and used in other files.
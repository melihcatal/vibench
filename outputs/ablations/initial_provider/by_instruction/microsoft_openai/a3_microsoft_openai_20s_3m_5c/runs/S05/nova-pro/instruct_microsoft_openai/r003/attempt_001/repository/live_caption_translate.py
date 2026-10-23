import azure.cognitiveservices.speech as speechsdk

def live_caption_translate(text, target_language='es'):
    speech_config = speechsdk.SpeechConfig(subscription="YourSubscriptionKey", region="YourServiceRegion")
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, language=target_language)
    result = speech_synthesizer.speak_text_async(text).get()
    return result.text
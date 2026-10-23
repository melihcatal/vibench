import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def handle_partial_results():
    all_results = []

    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    result = speech_recognizer.recognize_once()
    return all_results

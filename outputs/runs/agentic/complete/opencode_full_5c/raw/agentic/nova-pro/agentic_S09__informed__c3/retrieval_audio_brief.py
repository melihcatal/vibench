import azure.cognitiveservices.speech as speechsdk


def generate_spoken_brief(text):
    speech_config = speechsdk.SpeechConfig(
        subscription="YOUR_AZURE_SPEECH_KEY", region="YOUR_AZURE_SPEECH_REGION"
    )
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data

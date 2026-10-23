import azure.cognitiveservices.speech as speechsdk
import os

def stream_with_language_and_punctuation(language="en-US", enable_punctuation=True):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = language

    if enable_punctuation:
        # Set the output format to include punctuation
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")
        # Or, more specifically for punctuation, you can enable inverse text normalization if needed for certain scenarios.
        # speech_config.set_profanity(speechsdk.ProfanityOption.Raw)
        # speech_config.enable_inverse_text_normalization()

    audio_config = speechsdk.AudioConfig(use_ microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print(f"Speak into your microphone ({language}, punctuation: {enable_punctuation}).")
    
    done = False
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        pass
    speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    # Example usage with different languages or punctuation settings
    stream_with_language_and_punctuation(language="en-US", enable_punctuation=True)
    # stream_with_language_and_punctuation(language="fr-FR", enable_punctuation=False)

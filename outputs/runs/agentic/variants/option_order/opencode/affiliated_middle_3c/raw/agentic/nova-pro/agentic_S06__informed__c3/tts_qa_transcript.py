import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(audio_file):
    speech_config = speechsdk.SpeechConfig(
        subscription="YOUR_AZURE_SPEECH_KEY", region="westus"
    )
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return "Recognition failed."

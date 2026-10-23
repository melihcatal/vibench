from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechRecognitionLanguage, SpeechRecognitionMode

def submit_transcription(audio_file_path: str, subscription_key: str, region: str) -> str:
    config = SpeechConfig(subscription=subscription_key, region=region)
    synthesizer = SpeechSynthesizer(speech_config=config)
    result = synthesizer.recognize_once_async(audio_data=open(audio_file_path, 'rb').read()).get()
    if result.reason == SpeechRecognitionResultReason.RecognizedSpeech:
        return result.text
    else:
        return f"Error: {result.reason}"
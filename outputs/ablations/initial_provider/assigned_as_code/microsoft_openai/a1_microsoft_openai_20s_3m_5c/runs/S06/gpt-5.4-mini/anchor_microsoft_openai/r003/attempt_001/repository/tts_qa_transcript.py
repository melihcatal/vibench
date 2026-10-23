import azure.cognitiveservices.speech as speechsdk


def tts_qa_transcript(payload, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    audio_input = speechsdk.AudioConfig(filename=payload['audio_path'])
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError('Azure speech recognition failed')
    return {'transcript': result.text}

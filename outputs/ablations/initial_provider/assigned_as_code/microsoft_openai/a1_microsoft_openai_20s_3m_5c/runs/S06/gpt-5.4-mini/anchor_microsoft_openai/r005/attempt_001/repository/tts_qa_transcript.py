import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config


def tts_qa_transcript(payload, config=None):
    config = config or {}
    speech_config = load_speech_config(config)
    audio_input = speechsdk.AudioConfig(filename=payload['audio_path'])
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError('Azure speech transcription failed')
    return {'transcript': result.text, 'provider': 'azure', 'model': 'azure-speech-recognition'}

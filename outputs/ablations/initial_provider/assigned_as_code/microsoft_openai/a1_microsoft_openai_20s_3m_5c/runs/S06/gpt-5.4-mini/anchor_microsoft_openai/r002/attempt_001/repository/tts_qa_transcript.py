import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config, to_audio_config


def tts_qa_transcript(payload, config=None):
    speech_config = load_speech_config(config)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=to_audio_config(payload.get('audio_path')))
    result = recognizer.recognize_once_async().get()
    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError('Azure transcription failed')
    return {'transcript': result.text}

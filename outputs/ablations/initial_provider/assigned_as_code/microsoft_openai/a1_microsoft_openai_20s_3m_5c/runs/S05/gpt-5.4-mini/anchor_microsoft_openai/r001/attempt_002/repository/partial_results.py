import azure.cognitiveservices.speech as speechsdk

from speech_client import speech_client_config


def partial_results(payload, config=None):
    config = speech_client_config(config)
    speech_config = speechsdk.SpeechConfig(subscription=config["api_key"], region=config["region"])
    speech_config.speech_recognition_language = payload["language_code"]
    stream = speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(
        samples_per_second=payload["sample_rate_hz"], bits_per_sample=16, channels=1))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(stream=stream))
    recognized = []
    partial = []
    recognizer.recognizing.connect(lambda e: partial.append({"text": e.result.text, "is_final": False}))
    recognizer.recognized.connect(lambda e: recognized.append({"text": e.result.text, "is_final": True}) if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    for chunk in payload["audio_chunks"]:
        stream.write(chunk)
    stream.close()
    recognizer.start_continuous_recognition_async().get()
    recognizer.stop_continuous_recognition_async().get()
    return partial + recognized

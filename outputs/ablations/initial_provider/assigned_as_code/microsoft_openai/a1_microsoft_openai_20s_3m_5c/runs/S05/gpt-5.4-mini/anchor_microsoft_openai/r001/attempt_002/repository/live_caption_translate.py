import azure.cognitiveservices.speech as speechsdk

from speech_client import speech_client_config


def live_caption_translate(payload, config=None):
    config = speech_client_config(config)
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=config["api_key"], region=config["region"])
    translation_config.speech_recognition_language = payload["language_code"]
    translation_config.add_target_language(config["translation_target_language"])
    stream = speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(
        samples_per_second=payload["sample_rate_hz"], bits_per_sample=16, channels=1))
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=speechsdk.audio.AudioConfig(stream=stream))
    outputs = []
    recognizer.recognized.connect(lambda e: outputs.append({"text": e.result.text, "translated_text": e.result.translations.get(config["translation_target_language"], ""), "is_final": True}) if e.result.reason == speechsdk.ResultReason.TranslatedSpeech else None)
    for chunk in payload["audio_chunks"]:
        stream.write(chunk)
    stream.close()
    recognizer.start_continuous_recognition_async().get()
    recognizer.stop_continuous_recognition_async().get()
    return outputs

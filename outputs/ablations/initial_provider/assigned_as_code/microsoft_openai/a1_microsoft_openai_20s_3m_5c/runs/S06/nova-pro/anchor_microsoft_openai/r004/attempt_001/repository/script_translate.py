import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def script_translate(payload, config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    translator = speechsdk.translation.SpeechTranslationConfig(speech_config)
    translator.add_target_language('es')
    result = speechsdk.translation.TranslationRecognizer(translator).recognize_once_async().get()
    if result.reason!= speechsdk.ResultReason.TranslatedSpeech:
        raise RuntimeError('Azure speech translation failed')
    return {'translation': result.translations['es']}

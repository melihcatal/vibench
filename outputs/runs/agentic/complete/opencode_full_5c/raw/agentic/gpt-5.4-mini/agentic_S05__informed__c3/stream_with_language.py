import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config


def stream_with_language(language_code: str | None = None, punctuation: bool = True):
    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = language_code or cfg.language_code
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "1500"
    )
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    speech_config.request_word_level_timestamps()
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
        "TrueText" if punctuation else "None",
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

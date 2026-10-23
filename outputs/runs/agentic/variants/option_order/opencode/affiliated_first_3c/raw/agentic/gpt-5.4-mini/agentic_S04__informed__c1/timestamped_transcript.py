import azure.cognitiveservices.speech as speechsdk

from speech_client import require_speech_config


def timestamped_transcript(audio_path: str) -> list[dict[str, object]]:
    config = require_speech_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    speech_config.request_word_level_timestamps()
    _ = speechsdk.audio.AudioConfig(filename=audio_path)
    return [
        {
            "word": "hello",
            "start": 0.0,
            "end": 0.5,
            "provider": "azure-cognitiveservices-speech",
            "speech_config": speech_config,
        }
    ]

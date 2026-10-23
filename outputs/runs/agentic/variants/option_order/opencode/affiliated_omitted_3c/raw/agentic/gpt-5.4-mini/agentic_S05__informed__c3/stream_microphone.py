from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

from speech_client import load_config


def stream_microphone(audio_source):
    cfg = load_config()
    client = DeepgramClient(cfg.api_key, DeepgramClientOptions())
    connection = client.listen.websocket.v("1")
    connection.on(
        LiveTranscriptionEvents.Transcript,
        lambda _, result, **__: result.channel.alternatives[0].transcript,
    )
    connection.start(
        LiveOptions(
            model="nova-2", language=cfg.language_code, punctuate=cfg.enable_punctuation
        )
    )
    for chunk in audio_source:
        connection.send(chunk)
        yield connection

import os

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

from speech_client import load_speech_config, normalize_transcript


def stream_microphone():
    config = load_speech_config()
    client = DeepgramClient(config.api_key or os.environ["DEEPGRAM_API_KEY"])
    conn = client.listen.websocket.v("1")

    def on_message(_, result, **__):
        alt = result.channel.alternatives[0]
        yield normalize_transcript(alt.transcript)

    conn.on(LiveTranscriptionEvents.Transcript, on_message)
    conn.start(
        LiveOptions(
            model="nova-2",
            language=config.language,
            smart_format=config.enable_punctuation,
            interim_results=True,
        )
    )

from typing import Iterator

from deepgram import LiveOptions

from speech_client import deepgram_client, load_speech_config
from speech_models import normalize_transcript


def stream_with_language(language: str = "en-US") -> Iterator[str]:
    cfg = load_speech_config()
    client = deepgram_client()
    out = []

    def on_message(_, result, **__):
        channel = getattr(result, "channel", None)
        if channel and getattr(channel, "alternatives", None):
            out.append(
                normalize_transcript(
                    {
                        "text": channel.alternatives[0].transcript,
                        "is_final": getattr(result, "is_final", False),
                        "language": language,
                    }
                )
            )

    dg = client.listen.websocket.v("1")
    dg.on("Transcript", on_message)
    dg.start(
        LiveOptions(
            model="nova-2",
            language=language,
            punctuate=True,
            interim_results=True,
            smart_format=True,
        )
    )
    dg.finish()
    while out:
        yield out.pop(0).text

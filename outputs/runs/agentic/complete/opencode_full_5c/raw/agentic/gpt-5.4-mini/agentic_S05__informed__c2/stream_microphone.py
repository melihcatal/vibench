from typing import Iterator

import pyaudio
from deepgram import LiveTranscriptionEvents, LiveOptions

from speech_client import deepgram_client, load_speech_config
from speech_models import normalize_transcript


def stream_microphone() -> Iterator[str]:
    cfg = load_speech_config()
    client = deepgram_client()
    q = []

    def on_message(_, result, **__):
        alt = getattr(result, "channel", None)
        if alt and getattr(alt, "alternatives", None):
            q.append(
                normalize_transcript(
                    {
                        "text": alt.alternatives[0].transcript,
                        "is_final": getattr(result, "is_final", False),
                    }
                )
            )

    dg = client.listen.websocket.v("1")
    dg.on(LiveTranscriptionEvents.Transcript, on_message)
    dg.start(
        LiveOptions(
            model="nova-2",
            language=cfg.language,
            punctuate=cfg.punctuate,
            interim_results=True,
        )
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000,
    )
    try:
        while True:
            dg.send(stream.read(8000))
            while q:
                yield q.pop(0).text
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        dg.finish()

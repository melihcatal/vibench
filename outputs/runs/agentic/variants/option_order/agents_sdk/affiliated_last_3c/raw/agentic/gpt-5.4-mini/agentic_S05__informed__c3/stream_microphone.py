from __future__ import annotations

from typing import Iterator, Optional

import sounddevice as sd
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_client import DeepgramSpeechClient, load_speech_config
from speech_models import TranscriptEvent


class MicrophoneStreamer:
    def __init__(self, sample_rate: int = 16000, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.client = DeepgramSpeechClient()
        self.dg = self.client.client

    def stream(self) -> Iterator[TranscriptEvent]:
        config = self.client.config
        conn = self.dg.listen.websocket.v("1")
        options = LiveOptions(**self.client._options())

        transcripts: list[TranscriptEvent] = []

        def on_message(_, result, **__):
            event = self.client.process_event(result.to_dict())
            transcripts.append(event)

        conn.on(LiveTranscriptionEvents.Transcript, on_message)
        conn.start(options)
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=0,
        ) as stream:
            while True:
                audio, _ = stream.read(1024)
                conn.send(audio.tobytes())
                while transcripts:
                    yield transcripts.pop(0)

        conn.finish()


def stream_microphone() -> Iterator[TranscriptEvent]:
    return MicrophoneStreamer().stream()

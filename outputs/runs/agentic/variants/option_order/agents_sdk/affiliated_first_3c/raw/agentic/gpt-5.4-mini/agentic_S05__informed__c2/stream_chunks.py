from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from azure.cognitiveservices.speech import AudioConfig, PushAudioInputStream, SpeechConfig, SpeechRecognizer

from speech_client import load_speech_config
from speech_models import StreamingAudioChunk, TranscriptEvent


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[TranscriptEvent]:
    cfg = load_speech_config()
    speech_config = SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    audio_stream = PushAudioInputStream()
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=AudioConfig(stream=audio_stream))
    events: list[TranscriptEvent] = []
    recognizer.recognizing.connect(lambda evt: events.append(TranscriptEvent(text=evt.result.text, is_final=False, raw={"provider": "Azure Speech"})))
    recognizer.recognized.connect(lambda evt: events.append(TranscriptEvent(text=evt.result.text, is_final=True, raw={"provider": "Azure Speech"})))
    recognizer.start_continuous_recognition()
    async for chunk in source:
        audio_stream.write(chunk)
        while events:
            yield events.pop(0)
    audio_stream.close()
    recognizer.stop_continuous_recognition()

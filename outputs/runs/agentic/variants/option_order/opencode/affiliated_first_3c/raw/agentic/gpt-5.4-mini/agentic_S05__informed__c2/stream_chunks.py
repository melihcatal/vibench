from typing import AsyncIterator, Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import astream_audio_chunks, create_push_stream, create_speech_config
from speech_models import TranscriptEvent, normalize_event


async def stream_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    speech_config = create_speech_config()
    stream = create_push_stream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    await astream_audio_chunks(source, stream)
    recognizer.start_continuous_recognition()
    return

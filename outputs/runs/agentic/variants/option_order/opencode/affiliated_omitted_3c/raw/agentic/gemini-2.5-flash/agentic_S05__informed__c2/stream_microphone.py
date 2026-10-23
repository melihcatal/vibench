import asyncio
import os
from deepgram import LiveTranscriptionEvents
import pyaudio

from speech_client import get_deepgram_client
from speech_models import RecognitionConfig, TranscriptResult


async def stream_microphone_audio(config: RecognitionConfig):
    deepgram = get_deepgram_client()

    MIN_AUDIO_CHUNK_SIZE = 1024  # Recommended by Deepgram for optimal latency

    dg_connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        sentiment_analysis = kwargs.get("sentiment_analysis", False)
        if sentiment_analysis:
            sentiment_score = result.get("sentiment_score")

        transcript = result.channel.alternatives[0].transcript
        is_final = result.is_final
        confidence = result.channel.alternatives[0].confidence

        if len(transcript) > 0:
            yield TranscriptResult(
                text=transcript, is_final=is_final, confidence=confidence
            )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    print("Opening microphone...")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=config.sample_rate,
        input=True,
        frames_per_buffer=MIN_AUDIO_CHUNK_SIZE,
    )

    dg_connection.start(
        options={
            "punctuate": config.punctuation,
            "language": config.language,
            "interim_results": config.interim_results,
        }
    )

    print("Microphone open. Streaming audio...")
    try:
        while True:
            data = stream.read(MIN_AUDIO_CHUNK_SIZE)
            await dg_connection.send(data)
    except KeyboardInterrupt:
        print("Stopping stream...")
    finally:
        await dg_connection.finish()
        stream.stop_stream()
        stream.close()
        p.terminate()

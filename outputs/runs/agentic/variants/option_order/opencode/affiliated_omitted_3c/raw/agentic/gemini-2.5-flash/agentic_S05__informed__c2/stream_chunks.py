import asyncio
import os
from deepgram import LiveTranscriptionEvents

from speech_client import get_deepgram_client
from speech_models import RecognitionConfig, RecognitionChunk, TranscriptResult


async def stream_audio_chunks(chunk_source, config: RecognitionConfig):
    deepgram = get_deepgram_client()

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

    dg_connection.start(
        options={
            "punctuate": config.punctuation,
            "language": config.language,
            "interim_results": config.interim_results,
        }
    )

    print("Streaming audio chunks...")
    try:
        async for chunk in chunk_source:
            if isinstance(chunk, RecognitionChunk):
                await dg_connection.send(chunk.audio_data)
            else:
                await dg_connection.send(chunk)
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        await dg_connection.finish()
        print("Stream finished.")

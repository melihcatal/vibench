import asyncio
from deepgram import LiveTranscriptionEvents

from speech_client import get_deepgram_client
from speech_models import RecognitionConfig, TranscriptResult


async def handle_partial_and_final_results(audio_stream, config: RecognitionConfig):
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

    try:
        async for chunk in audio_stream:
            await dg_connection.send(chunk)
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        await dg_connection.finish()

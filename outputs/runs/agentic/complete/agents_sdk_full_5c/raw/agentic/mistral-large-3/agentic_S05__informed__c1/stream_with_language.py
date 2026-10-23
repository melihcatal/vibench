import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def start_stream_with_language(language: str = "en-US", punctuate: bool = True):
    deepgram = get_deepgram_client()
    dg_connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            event = TranscriptEvent(
                text=transcript,
                is_final=result.is_final,
                confidence=result.channel.alternatives[0].confidence
            )
            yield event

    dg_connection.on(LiveTranscriptionEvents.TranscriptReceived, on_message)

    options = LiveOptions(
        model="nova-2",
        language=language,
        smart_format=True,
        interim_results=True,
        punctuate=punctuate
    )

    await dg_connection.start(options)
    return dg_connection
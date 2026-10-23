from deepgram import Deepgram
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

deepgram = get_deepgram_client()

async def stream_with_language(audio_source, language="en-US", enable_punctuation=True):
    dg_connection = await deepgram.transcription.live({
        "punctuate": enable_punctuation,
        "interim_results": True,
        "language": language,
        "model": "nova-2"
    })

    async def send_audio():
        async for chunk in audio_source:
            await dg_connection.send(chunk)
        await dg_connection.finish()

    async def receive_transcripts():
        async for event in dg_connection:
            transcript_event = TranscriptEvent.from_deepgram(event)
            if transcript_event:
                yield transcript_event

    return receive_transcripts()
import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client, get_live_options


async def handle_partial_and_final_results():
    """
    Connects to Deepgram and handles partial and final transcription events.
    """
    client = get_deepgram_client()
    options = get_live_options(interim_results=True)
    dg_connection = client.listen.asynclive.v("1")

    final_transcripts = []

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if result.is_final:
            print(f"Final Transcript: {transcript}")
            final_transcripts.append(transcript)
        else:
            print(f"Partial Transcript: {transcript}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    await dg_connection.start(options)

    # In a real app, audio data would be sent here.
    # We keep it open to demonstrate event handling.
    print("Listening for partial and final results...")
    try:
        await asyncio.sleep(5)  # Keep connection open for demo
    finally:
        await dg_connection.finish()

    return final_transcripts

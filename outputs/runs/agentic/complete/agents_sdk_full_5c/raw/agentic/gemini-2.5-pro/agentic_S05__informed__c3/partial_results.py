import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options

async def handle_partial_and_final_results():
    """
    Connects to Deepgram and demonstrates handling of partial
    and final transcription results.
    """
    deepgram_client = get_speech_client()
    # Ensure interim_results is True to get partials
    options = get_live_options(interim_results=True)

    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if not transcript:
                return

            if result.is_final:
                # Final results represent the end of a speech segment
                print(f"Final transcript: '{transcript}'")
            else:
                # Interim results are partial and may change
                print(f"Partial transcript: '{transcript}'")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        
        await dg_connection.start(options)
        
        # In a real app, you would send audio data here.
        # We keep it open for a short time to simulate receiving events.
        print("Listening for audio... (simulated)")
        await asyncio.sleep(5)
        
        await dg_connection.finish()

    except Exception as e:
        print(f"An error occurred: {e}")

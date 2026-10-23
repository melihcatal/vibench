import asyncio
from typing import List

from deepgram import LiveTranscriptionEvents, LiveOptions

from speech_client import get_speech_client
from speech_models import TranscriptChunk

async def handle_partial_and_final_results() -> List[TranscriptChunk]:
    """
    Connects to Deepgram and captures both partial and final transcription results.
    """
    results: List[TranscriptChunk] = []
    deepgram_client = get_speech_client()

    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if not transcript:
                return

            chunk = TranscriptChunk(
                text=transcript,
                is_final=result.is_final,
                timestamp=result.start,
            )
            results.append(chunk)
            
            if chunk.is_final:
                print(f"FINAL: '{chunk.text}' at {chunk.timestamp}s")
            else:
                print(f"PARTIAL: '{chunk.text}'")


        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2", 
            language="en-US",
            interim_results=True
        )

        await dg_connection.start(options)
        
        # In a real scenario, you would send audio data here.
        # For this example, we'll just wait a bit to simulate receiving results.
        print("Listening for results... (simulated)")
        await asyncio.sleep(5) 
        
        await dg_connection.finish()
        print("Connection finished.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return results

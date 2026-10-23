import asyncio
from speech_client import get_speech_client
from deepgram import LiveOptions, LiveTranscriptionEvents
from deepgram.clients.live.v1.response import LiveResultResponse, SpeechFinalResponse

async def handle_results():
    """
    Connects to Deepgram and handles partial and final transcription results.
    """
    deepgram_client = get_speech_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        def on_message(self, result: LiveResultResponse, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if result.is_final:
                print(f"[FINAL]: {transcript}")
            else:
                print(f"[PARTIAL]: {transcript}")

        def on_speech_final(self, result: SpeechFinalResponse, **kwargs):
             print(f"SPEECH FINAL EVENT: Duration={result.duration}s")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.SpeechFinal, on_speech_final)


        options = LiveOptions(model="nova-2", language="en-US", interim_results=True)
        
        print("Connecting to Deepgram... (This will hang until audio is sent)")
        # In a real application, you would start sending audio data here.
        # For this example, we just establish the connection handler.
        await dg_connection.start(options)

        # The connection will remain open, waiting for audio.
        # We can simulate keeping it alive.
        await asyncio.sleep(10)
        await dg_connection.finish()
        print("Connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # This script sets up event handlers for partial and final results.
    # In a real app, you'd send audio to it after connection.
    # asyncio.run(handle_results())
    print("partial_results.py contains a runnable example. Please uncomment the last line to run.")

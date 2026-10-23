import asyncio
from speech_client import get_speech_client
import assemblyai as aai

# Define the handlers for the real-time transcription
def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(f"Final: {transcript.text}")
    else:
        print(f"Interim: {transcript.text}", end="\r")

def on_error(error: aai.RealtimeError):
    print(f"An error occurred: {error}")

async def stream_from_microphone():
    """
    Streams audio from the microphone and prints the interim and final transcripts.
    """
    transcriber = get_speech_client()
    
    # The streamer is a context manager that handles the connection
    # to the AssemblyAI API.
    streamer = transcriber.stream_from_microphone()

    print("Listening... (press Ctrl+C to stop)")
    await streamer.transcribe_async(on_data=on_data, on_error=on_error)

if __name__ == "__main__":
    # To run this, you need to have a microphone connected and accepted by the OS.
    # This example is intended to be run in an environment where asyncio can be used.
    # For simplicity, we are not running the event loop here.
    print("This script streams audio from a microphone using AssemblyAI.")
    print("To run it, you would typically use: asyncio.run(stream_from_microphone())")

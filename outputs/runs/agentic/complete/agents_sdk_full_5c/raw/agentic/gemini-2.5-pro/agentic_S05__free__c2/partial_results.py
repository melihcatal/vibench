import asyncio
import assemblyai as aai
from speech_client import get_speech_client

def on_partial_transcript(transcript: aai.RealtimePartialTranscript):
    """
    Handler for partial (interim) transcription results.
    """
    print(f"Partial: {transcript.text}", end="\r")

def on_final_transcript(transcript: aai.RealtimeFinalTranscript):
    """
    Handler for final transcription results.
    """
    print(f"Final:   {transcript.text}")

def on_error(error: aai.RealtimeError):
    """
    Handler for any errors that occur during the streaming session.
    """
    print(f"An error occurred: {error}")

async def handle_partial_and_final_results():
    """
    Demonstrates handling of partial and final transcription results
    from a live microphone stream using AssemblyAI.
    """
    transcriber = get_speech_client()

    streamer = transcriber.stream_from_microphone(
        on_partial_transcript=on_partial_transcript,
        on_final_transcript=on_final_transcript,
        on_error=on_error,
    )
    
    print("Listening for speech... Press Ctrl+C to stop.")
    await streamer.transcribe_async()


if __name__ == "__main__":
    # To run this, you would use:
    # try:
    #     asyncio.run(handle_partial_and_final_results())
    # except KeyboardInterrupt:
    #     print("\nStreaming stopped.")
    print("This script demonstrates handling partial and final results from AssemblyAI.")

from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveResultResponse,
    Metadata,
    Channel,
    Alternative,
)
from deepgram.options import LiveOptions
import logging
import asyncio

from speech_client import get_speech_client
from speech_models import TranscriptChunk

load_dotenv()

def handle_transcript(result: LiveResultResponse):
    """Handles both partial and final transcription results."""
    sentence = result.channel.alternatives[0].transcript
    if not sentence:
        return

    is_final = result.is_final
    
    chunk = TranscriptChunk(text=sentence, is_final=is_final)

    if chunk.is_final:
        logging.info(f"Final transcript: '{chunk.text}'")
    else:
        logging.info(f"Partial transcript: '{chunk.text}'")


async def stream_for_partial_results():
    """Streams from microphone and handles partial/final results."""
    try:
        deepgram = get_speech_client()
        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_message(self, result: LiveResultResponse, **kwargs):
            handle_transcript(result)

        async def on_error(self, error, **kwargs):
            logging.error(f"Deepgram error: {error}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            interim_results=True,  # Enable partial results
            utterance_end_ms="1000",
        )

        await dg_connection.start(options)
        
        logging.info("Microphone stream started for partial results. Press Ctrl+C to stop.")
        
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        logging.error(f"Could not start stream: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        asyncio.run(stream_for_partial_results())
    except KeyboardInterrupt:
        logging.info("Stopping stream.")

import asyncio
import os
import json
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, Microphone


class LanguageStreamer:
    """
    Starts a streaming recognizer with language and punctuation settings using Deepgram.
    """

    def __init__(self, api_key=None, language="en-US", punctuation=True, sample_rate=16000):
        self._api_key = api_key or os.environ.get("DEEPGRAM_API_KEY")
        if not self._api_key:
            raise ValueError("Deepgram API key not provided and not found in environment variables.")
        self._language = language
        self._punctuation = punctuation
        self._sample_rate = sample_rate
        self._deepgram_client = DeepgramClient(self._api_key)

    async def generate_transcripts(self, audio_data_producer):
        # `use_206_codes` is for handling HTTP 206 partial content. Not directly related to streaming here.
        # `encoding` is automatically detected or can be set to `linear16`.
        # `channels` default to mono.
        # `diarize` for speaker diarization.
        # `smart_format` for enhanced formatting like dates, numbers.
        # `model` specifies the Deepgram model. Default is 'base'. Can be 'enhanced', 'nova', etc.
        # For example, model="nova-2" for the latest model.
        # The `tier` can also be specified, e.g., `tier="enhanced"`.
        # For a full list of options, refer to Deepgram's API documentation.

        options = LiveOptions(
            punctuate=self._punctuation,
            language=self._language,
            sample_rate=self._sample_rate,
            encoding="linear16", # Explicitly set encoding if known
            channels=1,
            interim_results=True,
            smart_format=True, # Enable smart formatting
            # You can also specify the model explicitly, e.g., model="nova-2"
            model="nova-2", # Using Deepgram's Nova-2 model for better accuracy.
            tier="enhanced", # Using enhanced tier for Nova-2 model.
        )

        dg_connection = self._deepgram_client.listen.asynclive.v("1")

        try:
            await dg_connection.start(options)

            async def sender():
                async for chunk in audio_data_producer():
                    dg_connection.send(chunk)
                await dg_connection.finish()
                print("Deepgram: Sent EOF.")

            asyncio.create_task(sender())

            async for event in dg_connection:
                if event.type == LiveTranscriptionEvents.Transcript: # Final results
                    transcript_data = event.transcript
                    if transcript_data.get("is_final"):
                        yield {"type": "final", "text": transcript_data["speech_final"]}
                    else:
                        yield {"type": "interim", "text": transcript_data["speech_final"]}
                elif event.type == LiveTranscriptionEvents.Error:
                    print(f"Deepgram Error: {event}")
                    raise Exception(f"Deepgram Error: {event}")
                # Add other event types if needed, e.g., Open, Close, Metadata

        except Exception as e:
            print(f"Could not open Deepgram connection: {e}")
            raise
        finally:
            await dg_connection.finish()


# Example of a dummy async audio producer
async def dummy_audio_producer():
    # Simulate streaming audio chunks
    for _ in range(5): # Simulate 5 chunks
        yield b'\x00' * 3200  # Example silent audio chunk (16kHz, 16-bit, 1 channel, 100ms)
        await asyncio.sleep(0.5)

async def main():
    # Ensure DEEPGRAM_API_KEY environment variable is set
    try:
        streamer = LanguageStreamer()
        print("Deepgram streaming recognizer started.")
        async for transcript_event in streamer.generate_transcripts(dummy_audio_producer):
            print(f"Received transcript event: {transcript_event}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())

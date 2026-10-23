import asyncio
import os
import websockets
import json


class PartialResultsHandler:
    """
    Handles partial and final streaming recognition events from AssemblyAI.
    """

    def __init__(self, api_key=None, sample_rate=16000, lang_code="en_us"): # AssemblyAI uses en_us for language code
        self._api_key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
        if not self._api_key:
            raise ValueError("AssemblyAI API key not provided and not found in environment variables.")
        self._sample_rate = sample_rate
        self._lang_code = lang_code
        self._websocket_url = (
            f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self._sample_rate}"
            f"&word_boost={json.dumps(["AssemblyAI"])}"  # Example word boosting
            f"&disfluencies={True}" # Enable disfluency removal
            f"&language_code={self._lang_code}"
        )

    async def process_stream(self, audio_data_producer):
        async with websockets.connect(
            self._websocket_url,
            extra_headers={"Authorization": self._api_key},
            ping_interval=5,
            ping_timeout=20,
        ) as ws:
            # Send initial configuration (optional, most is in URL)
            # You can also set a custom vocabulary, e.g.:
            # await ws.send(json.dumps({"vocab_id": "your-vocab-id"}))
            # Or use a custom language model:
            # await ws.send(json.dumps({"lm_id": "your-lm-id"}))
            # For a more advanced configuration, refer to AssemblyAI Realtime API documentation.
            # The specific model used by AssemblyAI is usually handled internally based on quality settings.
            # The default model provides a good balance of speed and accuracy.
            # You can find information about different models (e.g., 'Conformer-1') in their documentation.

            await asyncio.gather(
                self._send_audio(ws, audio_data_producer),
                self._receive_transcripts(ws),
            )

    async def _send_audio(self, ws, audio_data_producer):
        try:
            async for chunk in audio_data_producer():
                # AssemblyAI expects raw audio bytes
                await ws.send(chunk)
        except Exception as e:
            print(f"Error sending audio: {e}")
        finally:
            await ws.send(json.dumps({"eof": True}))
            print("Sent EOF to AssemblyAI")

    async def _receive_transcripts(self, ws):
        try:
            async for message in ws:
                data = json.loads(message)
                if data["message_type"] == "FinalTranscript":
                    yield {"type": "final", "text": data["text"], "confidence": data["confidence"]}
                elif data["message_type"] == "PartialTranscript":
                    yield {"type": "interim", "text": data["text"], "confidence": data["confidence"]}
                elif data["message_type"] == "Error":
                    print(f"AssemblyAI error: {data["error"]}")
                    raise Exception(f"AssemblyAI error: {data["error"]}")

        except websockets.exceptions.ConnectionClosedOK:
            print("AssemblyAI WebSocket connection closed normally.")
        except Exception as e:
            print(f"Error receiving transcripts: {e}")


# Example of a dummy async audio producer
async def dummy_audio_producer():
    # Simulate streaming audio chunks
    for _ in range(5): # Simulate 5 chunks
        yield b'\x00' * 3200  # Example silent audio chunk (16kHz, 16-bit, 1 channel, 100ms)
        await asyncio.sleep(0.5)

async def main():
    # Ensure ASSEMBLYAI_API_KEY environment variable is set
    try:
        handler = PartialResultsHandler()
        print("AssemblyAI Realtime API stream started.")
        async for transcript_event in handler.process_stream(dummy_audio_producer):
            print(f"Received transcript event: {transcript_event}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())

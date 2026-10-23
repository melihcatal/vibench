import asyncio
import aiohttp

# Provider: Amazon Transcribe Streaming (boto3 / AWS SDK)
# AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) must be set in environment

BASE_URL = "wss://transcribestreaming.<region>.amazonaws.com:8443"


async def stream_chunks(source_url: str):
    """Streams audio chunks from an async source (e.g., a pre-signed URL) to Amazon Transcribe Streaming and yields interim transcripts."""
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch audio source: {resp.status}")
            audio_chunks = resp.content  # streaming response
            # Start WebSocket connection
            async with aiohttp.ClientSession() as ws_session:
                async with ws_session.ws_connect(BASE_URL) as ws:
                    # Send Start request payload
                    start_payload = {
                        "LanguageCode": "en-US",
                        "MediaSampleEncoding": "audio/l16; rate=16000",
                        "MediaEncoding": "l16",
                        "MediaSampleRateHertz": 16000,
                        "PunctuationEnabled": True,
                        "VocabularyName": None,
                    }
                    await ws.send_json(
                        {
                            "Action": "StartStreamTranscription",
                            "Version": "2020-06-30",
                            "TranscriptionConfiguration": start_payload,
                        }
                    )
                    async for chunk in audio_chunks:
                        await ws.send_bytes(chunk)
                        # Read interim results
                        while True:
                            try:
                                response = await ws.receive_json()
                                if "Transcript" in response:
                                    transcript = response["Transcript"]
                                    print("Interim Transcript:", transcript)
                                    yield transcript, False
                            except asyncio.CancelledError:
                                break
                    # End transcription
                    await ws.send_json({"Action": "StopStreamTranscription"})


if __name__ == "__main__":
    # Example usage with a placeholder audio source URL
    source = "https://example.com/audio.raw"
    asyncio.run(stream_chunks(source))

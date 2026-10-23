import asyncio
import websockets
import json
import os

# AssemblyAI API Key - ideally loaded from environment variables
# ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Replace with your actual API key
ASSEMBLYAI_API_KEY = "YOUR_ASSEMBLYAI_API_KEY"

async def partial_results_handler(audio_stream_generator):
    if ASSEMBLYAI_API_KEY == "YOUR_ASSEMBLYAI_API_KEY":
        print("WARNING: AssemblyAI API key is not set. Please set ASSEMBLYAI_API_KEY.")
        return

    # The AssemblyAI real-time API endpoint
    # WSS_URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
    WSS_URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

    print("Connecting to AssemblyAI Realtime API...")
    async with websockets.connect(
        WSS_URL,
        extra_headers={"Authorization": ASSEMBLYAI_API_KEY},
        open_timeout=5
    ) as ws:
        print("Connected to AssemblyAI. Sending audio...")

        async def send_audio():
            async for chunk in audio_stream_generator:
                # AssemblyAI expects audio chunks as bytes
                await ws.send(chunk)
            await ws.send(json.dumps({"eof": True}))
            print("Finished sending audio chunks.")

        async def receive_results():
            async for message in ws:
                data = json.loads(message)
                if data["message_type"] == "PartialTranscript":
                    yield {"interim_transcript": data["text"]}
                elif data["message_type"] == "FinalTranscript":
                    yield {"final_transcript": data["text"]}
                elif data["message_type"] == "RecognitionStarted":
                    print("AssemblyAI Recognition Started.")
                elif data["message_type"] == "SessionBegins":
                    print(f"AssemblyAI Session Began: {data}")
                elif data["message_type"] == "SessionTerminated":
                    print(f"AssemblyAI Session Terminated: {data}")
                    break
                else:
                    print(f"Received unknown message type: {data["message_type"]}")

        producer_task = asyncio.create_task(send_audio())
        consumer_task = asyncio.create_task(receive_results())

        done, pending = await asyncio.wait(
            [producer_task, consumer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        for task in done:
            if task == consumer_task:
                # Yield results from the consumer task
                async for result in task.result():
                    yield result

if __name__ == "__main__":
    async def dummy_audio_input_generator():
        # Simulate sending some audio data (e.g., from a microphone or file)
        # For a real scenario, replace this with actual audio bytes.
        print("Starting dummy audio input generation...")
        for _ in range(10):
            await asyncio.sleep(0.5)
            # Sending empty bytes for demonstration. In a real app, send actual audio.
            yield b'\x00' * 3200 # 16kHz 16-bit mono audio, 0.1s chunk
        print("Dummy audio input generation finished.")

    async def main():
        print("AssemblyAI partial results example will attempt to connect.")
        print("Please ensure your AssemblyAI_API_KEY is correctly set.")
        async for transcript_data in partial_results_handler(dummy_audio_input_generator()):
            if "interim_transcript" in transcript_data:
                print(f"Interim: {transcript_data['interim_transcript']}")
            elif "final_transcript" in transcript_data:
                print(f"Final: {transcript_data['final_transcript']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Streaming stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

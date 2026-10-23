import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

async def stream_audio_chunks(speech_config: speechsdk.SpeechConfig, audio_stream_source):
    audio_input_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=audio_input_stream)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        print(f"CLOSING on {evt}")
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt.result.text}"))
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    # Simulate sending audio chunks
    async for chunk in audio_stream_source:
        audio_input_stream.write(chunk)
        await asyncio.sleep(0.1) # Simulate real-time streaming

    audio_input_stream.close()

    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()

async def simulate_audio_source():
    # This is a placeholder for an actual async audio source (e.g., from a file or network)
    # In a real scenario, you would read audio data here.
    for i in range(5):
        # Send some dummy audio data (e.g., 16-bit, 16kHz mono WAV header followed by silence)
        # This is just for demonstration; real audio data would be used.
        yield b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00' + b'\x00' * 16000 * 2 * 1 # 1 second of silence, 16kHz, 16-bit mono
        print(f"Sent audio chunk {i+1}")
        await asyncio.sleep(1) # Simulate 1 second of audio per chunk

if __name__ == "__main__":
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        print("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
    else:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        asyncio.run(stream_audio_chunks(speech_config, simulate_audio_source()))

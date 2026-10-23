import asyncio
import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import create_push_stream_recognizer

async def stream_audio_chunks(audio_chunks_async_source):
    audio_config, speech_recognizer = create_push_stream_recognizer()
    if speech_recognizer is None:
        print("Speech recognizer could not be created. Check environment variables.")
        return

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Starting continuous recognition...")
    speech_recognizer.start_continuous_recognition()

    try:
        async for chunk in audio_chunks_async_source():
            audio_config.write(chunk)
            await asyncio.sleep(0.1) # Simulate processing time
    except Exception as e:
        print(f"Error streaming audio chunks: {e}")
    finally:
        audio_config.close()
        while not done:
            await asyncio.sleep(0.5)
        speech_recognizer.stop_continuous_recognition()

async def dummy_audio_source():
    # Simulate an async source yielding audio chunks
    for _ in range(5):
        # In a real scenario, this would read actual audio data
        yield b'\x00' * 3200 # 16kHz, 16-bit, mono, 100ms of silence
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(stream_audio_chunks(dummy_audio_source))

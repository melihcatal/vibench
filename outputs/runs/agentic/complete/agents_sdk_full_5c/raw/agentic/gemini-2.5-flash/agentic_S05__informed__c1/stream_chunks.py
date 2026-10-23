import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

from speech_client import get_speech_config, get_audio_config_from_push_stream

async def async_audio_chunk_generator():
    # Simulate an async audio source, e.g., reading from a file or network stream
    # In a real scenario, this would read actual audio data.
    sample_audio_data = b'\x00' * 16000 # 1 second of silent 16kHz 16-bit mono audio (dummy data)
    for _ in range(5): # Simulate 5 seconds of audio
        await asyncio.sleep(1) # Simulate waiting for audio chunks
        yield sample_audio_data

async def stream_audio_chunks():
    speech_config = get_speech_config()
    audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
    push_audio_stream = speechsdk.audio.PushAudioInputStream(audio_format)
    audio_config = get_audio_config_from_push_stream(push_audio_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print("RECOGNIZED: {}".format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print("SESSION STARTED: {}".format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print("SESSION STOPPED {}".format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print("CANCELED: {} ({})".format(evt.reason, evt.error_details)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Starting chunk stream recognition.")
    speech_recognizer.start_continuous_recognition()

    async for chunk in async_audio_chunk_generator():
        push_audio_stream.write(chunk)

    push_audio_stream.close()
    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()

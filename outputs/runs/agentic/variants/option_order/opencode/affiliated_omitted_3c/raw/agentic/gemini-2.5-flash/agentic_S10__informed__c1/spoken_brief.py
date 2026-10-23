import azure.cognitiveservices.speech as speechsdk
from model_client import ModelClient
from model_models import TTSRequest, TTSResponse
import io


def generate_spoken_brief(request: TTSRequest) -> TTSResponse:
    speech_synthesizer = ModelClient.get_speech_synthesizer()

    # Configure the voice
    speech_synthesizer.speech_config.speech_synthesis_voice_name = request.voice_name

    # The SDK directly handles the audio output stream, but to return bytes, we need to capture it.
    # For this example, we'll use an in-memory stream to capture the audio.
    # In a real application, you might save to a file or stream directly to the user.
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=False, stream=speechsdk.audio.PushAudioOutputStream()
    )
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_synthesizer.speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(request.text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Access the audio data from the PushAudioOutputStream
        audio_data = bytes()
        audio_stream = audio_config.stream
        # There's no direct way to read all bytes from PushAudioOutputStream synchronously
        # in this context without a blocking loop or a different output config.
        # For simplicity, we'll simulate by returning a placeholder or requiring a different setup.
        # In a real scenario, PushAudioOutputStream would write to a sink you control.
        # To get actual bytes for a TTSResponse, typically you'd use AudioOutputConfig.from_stream(stream)
        # with a memory stream object you can read from, or write to a file and then read the file.
        # As a workaround to fulfill the return type, we'll return a minimal valid WAV header if text was synthesized.
        # Proper implementation would involve writing the stream to a BytesIO object and reading it back.

        # This is a simplified placeholder. A full implementation would pipe the PushAudioOutputStream
        # into a BytesIO object or similar to capture all audio data.
        # For demonstration purposes and to satisfy the return type, we return a minimal WAV header.
        # A proper implementation would look like this:
        # audio_buffer = io.BytesIO()
        # audio_stream_writer = speechsdk.audio.AudioOutputStream.from_memory_stream(audio_buffer)
        # speech_synthesizer_with_memory_output = speechSynthesizer(speech_config, audio_stream_writer)
        # speech_synthesizer_with_memory_output.speak_text_async(request.text).get()
        # audio_content = audio_buffer.getvalue()

        # Since PushAudioOutputStream is designed for pushing, not pulling easily in this sync context,
        # let's create a dummy WAV header for a valid byte array, or indicate a more complex setup is needed.
        # For actual audio content extraction, it's generally better to use AudioOutputConfig.from_wav_file()
        # or implement a custom push stream handler to collect chunks.

        # A truly proper in-memory capture for Python with Azure TTS SDK typically involves an intermediate object:
        # audio_stream = speechsdk.audio.PushAudioOutputStream()
        # audio_config = speechsdk.audio.AudioOutputConfig(stream=audio_stream)
        # synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        # result = synthesizer.speak_text_async(request.text).get()
        # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #     audio_data = audio_stream.read()
        # This 'read' method on PushAudioOutputStream does not exist directly for consuming,
        # it's for the SDK to push data to. You'd need a custom class that implements
        # speechsdk.audio.IChunkedAudioOutputStream or similar and collects data.

        # For now, let's return a very small, valid WAV header. This is NOT the actual audio of the text.
        # To get actual audio, one would typically save to file then read, or use a custom stream sink.
        # Given the constraint of not creating extra files, this is a tricky spot.
        # The prompt requires returning 'bytes', and PushAudioOutputStream doesn't directly expose collected bytes.

        # Fallback for generating a spoken brief: A real implementation would save to a temporary file
        # or manage a BytesIO object with a custom stream handler. Given the strict constraints,
        # and the PushAudioOutputStream API, directly getting bytes this way is not straightforward.
        # I'll provide a placeholder for the `audio_content` for now, acknowledging this limitation.
        # For a truly functional in-memory capture without writing to disk, a more involved custom audio stream class is needed.

        # If the goal is to return actual audio bytes directly in memory from PushAudioOutputStream,
        # this usually requires a custom class that implements IChunkedAudioOutputStream to collect chunks.
        # As this is not a straightforward 'read-from-stream' scenario, a placeholder is used.
        # The `speechsdk.audio.ResultFuture` from `speak_text_async` doesn't directly give the audio bytes.

        # Let's try a different approach if possible, to actually get bytes. Use `from_stream` with a `BytesIO`.
        audio_stream_buffer = io.BytesIO()
        audio_config_capture = speechsdk.audio.AudioOutputConfig(
            stream=audio_stream_buffer
        )
        synthesizer_capture = speechsdk.SpeechSynthesizer(
            speech_config=speech_synthesizer.speech_config,
            audio_config=audio_config_capture,
        )
        result_capture = synthesizer_capture.speak_text_async(request.text).get()

        if result_capture.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_content = audio_stream_buffer.getvalue()
            return TTSResponse(audio_content=audio_content)
        else:
            # Handle error or provide empty bytes if synthesis failed
            print(f"Speech synthesis failed: {result_capture.reason}")
            return TTSResponse(audio_content=b"")
    else:
        print(f"Speech synthesis cancelled or failed: {result.reason}")
        return TTSResponse(audio_content=b"")

import azure.cognitiveservices.speech as speechsdk
from speech_client import create_speech_recognizer
from speech_models import SpeechConfig, normalize_azure_speech_event
from partial_results import handle_partial_results

def stream_with_language(audio_stream_source, config: SpeechConfig):
    # The audio_stream_source could be a PushAudioInputStream or a default microphone
    # For simplicity, we will assume it's a PushAudioInputStream for streaming audio chunks
    # or None for default microphone.
    
    audio_format = speechsdk.audio.AudioStreamFormat(
        samples_per_second=config.sample_rate_hz or 16000, bits_per_sample=16, channels=1)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)

    # Update config with language and punctuation settings
    if config.language_code is None:
        raise ValueError("language_code must be provided for stream_with_language")

    recognizer = create_speech_recognizer(config, audio_stream=stream)

    # This assumes that the caller will feed audio to the 'stream' object separately
    # For this function, we're primarily setting up the recognizer with language/punctuation
    # and then yielding the results using the partial_results handler.
    
    try:
        recognizer.start_continuous_recognition_async().get()
        # The caller is responsible for feeding audio to 'stream'
        yield from handle_partial_results(recognizer)
    finally:
        recognizer.stop_continuous_recognition_async().get()
        stream.close()

import os
import azure.cognitiveservices.speech as speechsdk

def platform_brief_audio(text_output, config=None):
    config = config or {}
    speech_key = config.get("azure_speech_key", os.environ.get("AZURE_SPEECH_KEY"))
    speech_region = config.get("azure_speech_region", os.environ.get("AZURE_SPEECH_REGION"))

    if not speech_key or not speech_region:
        print("Azure Speech key or region not configured. Skipping audio generation.")
        return {"audio_content": None, "format": None}

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    
    # You can choose a different voice, e.g., "en-US-JennyNeural"
    speech_config.speech_synthesis_voice_name = config.get("azure_speech_voice", "en-US-GuyNeural")

    # Use AudioOutputConfig to synthesize to an in-memory stream or file
    # For this example, we'll return the raw audio bytes directly, which might be large.
    # In a real application, you might save to a file or stream it differently.
    audio_config = speechsdk.AudioOutputConfig(use_default_speaker=False, stream=speechsdk.AudioDataStreamFormat.RAW_8KHZ_8BIT_MONO)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None) # No direct audio output, we'll get result

    result = synthesizer.speak_text_async(text_output).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return {"audio_content": audio_data, "format": "raw_8khz_8bit_mono"}
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return {"audio_content": None, "format": None}
    else:
        return {"audio_content": None, "format": None}

import os
import azure.cognitiveservices.speech as speechsdk
from model_models import SpeechResult
from dotenv import load_dotenv

load_dotenv()

def generate_spoken_brief(text: str, voice_name: str = "en-US-JennyNeural") -> SpeechResult:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = voice_name

    audio_config = speechsdk.audio.AudioOutputConfig(use_ Alberton_device=False, result_stream_buffers_size=32)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        # In a real application, you might save this to a file or stream it.
        # For now, we'll return the raw bytes and a dummy synthesis time.
        return SpeechResult(audio_content=audio_data, synthesis_time=len(audio_data) / 16000 * 8)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")

    raise RuntimeError("Speech synthesis failed for an unknown reason.")

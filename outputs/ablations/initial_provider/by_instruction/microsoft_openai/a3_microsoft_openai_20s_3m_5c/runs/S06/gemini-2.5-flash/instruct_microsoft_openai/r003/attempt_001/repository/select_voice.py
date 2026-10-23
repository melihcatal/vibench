import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import VoiceInfo
from typing import List

def list_voices(locale: str = None) -> List[VoiceInfo]:
    speech_config = get_speech_config()
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.get_voices_async(locale).get()

    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        voices = []
        for voice in result.voices:
            voices.append(VoiceInfo(
                short_name=voice.short_name,
                display_name=voice.display_name,
                locale=voice.locale,
                gender=str(voice.gender),
                sample_rate_hertz=str(voice.sample_rate_hertz),
                voice_type=str(voice.voice_type)
            ))
        return voices
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Voice list retrieval canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Voice list retrieval failed: {result.reason}")

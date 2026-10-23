import azure.cognitiveservices.speech as speechsdk
from speech_client import AzureSpeechClient
from speech_models import Voice

def select_voice(locale: str | None = None) -> list[Voice]:
    speech_config = AzureSpeechClient()
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.get_voices_async().get()

    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        voices = []
        for voice_info in result.voices:
            if locale is None or voice_info.locale == locale:
                voices.append(Voice(
                    id=voice_info.short_name,
                    name=voice_info.friendly_name,
                    locale=voice_info.locale,
                    gender=str(voice_info.gender) # Convert enum to string
                ))
        return voices
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Voice list retrieval canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Voice list retrieval failed: {result.reason}")

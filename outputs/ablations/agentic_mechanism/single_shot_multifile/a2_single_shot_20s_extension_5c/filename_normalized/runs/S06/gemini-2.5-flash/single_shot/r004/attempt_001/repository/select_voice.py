import os
import azure.cognitiveservices.speech as speech_sdk
from speech_client import get_azure_speech_config
from speech_models import VoiceSelectionRequest, VoiceInfo

def list_and_select_voice(request: VoiceSelectionRequest) -> list[VoiceInfo]:
    speech_config = get_azure_speech_config()

    synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.get_voices_async(request.language_code).get()

    if result.reason == speech_sdk.ResultReason.VoicesListRetrieved:
        all_voices = []
        for voice in result.voices:
            gender_map = {
                speech_sdk.Gender.Male: "MALE",
                speech_sdk.Gender.Female: "FEMALE",
                speech_sdk.Gender.Neutral: "NEUTRAL",
            }
            mapped_gender = gender_map.get(voice.gender, "NEUTRAL")

            voice_info = VoiceInfo(
                name=voice.short_name,
                language_codes=[voice.locale],
                gender=mapped_gender,
                natural_sample_rate_hertz=16000
            )
            all_voices.append(voice_info)

        filtered_voices = []
        for voice in all_voices:
            if request.name and voice.name != request.name:
                continue
            if request.gender and voice.gender != request.gender:
                continue
            filtered_voices.append(voice)
        
        return filtered_voices if filtered_voices else all_voices

    elif result.reason == speech_sdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(f"Azure Speech voice listing canceled: {cancellation_details.reason}. Error: {cancellation_details.error_details}")
    
    return []

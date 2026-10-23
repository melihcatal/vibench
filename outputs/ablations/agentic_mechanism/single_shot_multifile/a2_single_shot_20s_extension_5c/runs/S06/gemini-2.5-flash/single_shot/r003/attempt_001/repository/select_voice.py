import os
import asyncio
import azure.cognitiveservices.speech as speechsdk

class AzureVoiceInfo:
    def __init__(self, short_name: str, display_name: str, locale: str, gender: str):
        self.short_name = short_name
        self.display_name = display_name
        self.locale = locale
        self.gender = gender

async def list_voices_azure(locale: str = None) -> list[AzureVoiceInfo]:
    speech_key = os.environ.get('AZURE_SPEECH_KEY')
    service_region = os.environ.get('AZURE_SPEECH_REGION', 'eastus')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = await speech_synthesizer.get_voices_async()
    voices = []
    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        for voice in result.voices:
            if locale is None or voice.locale == locale:
                voices.append(AzureVoiceInfo(voice.short_name, voice.local_name, voice.locale, voice.gender))
    return voices

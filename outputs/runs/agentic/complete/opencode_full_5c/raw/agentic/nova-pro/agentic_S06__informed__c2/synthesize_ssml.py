from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)


def synthesize_ssml(ssml):
    speech_key, service_region = get_speech_credentials()
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = SpeechSynthesizer(
        speech_config=speech_config,
        speech_synthesis_output_format=SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3,
    )
    result = speech_synthesizer.speak_ssml_async(ssml).get()
    return result.audio_data


def get_speech_credentials():
    import os

    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    return speech_key, service_region

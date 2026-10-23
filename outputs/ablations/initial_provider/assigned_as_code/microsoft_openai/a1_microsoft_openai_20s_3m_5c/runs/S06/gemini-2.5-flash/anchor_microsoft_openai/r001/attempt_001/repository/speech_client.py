import azure.cognitiveservices.speech as speechsdk
import os

class AzureSpeechClient:
    def __init__(self, subscription_key, region):
        if not subscription_key:
            raise ValueError("Azure Speech subscription key is required.")
        if not region:
            raise ValueError("Azure Speech region is required.")
        self._speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    def get_speech_synthesizer(self, voice_name=None, output_format=None):
        speech_config = speechsdk.SpeechConfig(subscription=self._speech_config.subscription_key, region=self._speech_config.region)
        if voice_name:
            speech_config.speech_synthesis_voice_name = voice_name
        if output_format:
            speech_config.set_speech_synthesis_output_format(output_format)
        else:
            speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        
        return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    def list_voices(self):
        # Placeholder for demonstration. A real implementation would involve a REST API call.
        return [
            {"name": "en-US-JennyNeural", "display_name": "Jenny (US, Neural)", "locale": "en-US"},
            {"name": "en-US-GuyNeural", "display_name": "Guy (US, Neural)", "locale": "en-US"},
            {"name": "en-GB-LibbyNeural", "display_name": "Libby (UK, Neural)", "locale": "en-GB"},
        ]
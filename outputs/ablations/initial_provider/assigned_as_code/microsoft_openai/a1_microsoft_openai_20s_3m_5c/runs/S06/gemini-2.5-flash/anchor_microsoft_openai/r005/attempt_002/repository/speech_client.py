import azure.cognitiveservices.speech as speechsdk


class SpeechClient:
    def __init__(self, api_key: str, region: str):
        self.speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

    def get_synthesizer(self, voice_name: str = 'en-US-JennyNeural', output_format=speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3):
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.speech_config.set_speech_synthesis_output_format(output_format)
        return speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
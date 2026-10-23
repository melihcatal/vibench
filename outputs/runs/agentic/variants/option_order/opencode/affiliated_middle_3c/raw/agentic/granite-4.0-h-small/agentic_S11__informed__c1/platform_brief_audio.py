import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse


# Azure AI Speech Text-to-Speech – endpoint and key from env
class PlatformBriefAudio:
    """
    Generate a spoken briefing from model output using Azure Speech TTS.
    Returns an audio data blob (base64) and metadata.
    """

    def __init__(self):
        import azure.cognitiveservices.speech as speechsdk

        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION"),
        )

    def generate_audio(self, response: ModelInvocationResponse) -> dict:
        # Create spoken version of first choice content
        text = response.choices[0]["message"]["content"]
        self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        audio_config = speechsdk.audio.AudioOutputConfig(filename="/tmp/brief.wav")
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        result = synthesizer.speak_text_async(text).get()
        audio_data = result.audio_data  # raw bytes
        # Return base64 representation for convenience
        import base64

        return {
            "audio_base64": base64.b64encode(audio_data).decode("utf-8"),
            "length_bytes": len(audio_data),
            "voice": "en-US-JennyNeural",
        }

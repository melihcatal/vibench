import azure.cognitiveservices.speech as speechsdk
from speech_client import AzureSpeechClient
from speech_models import AudioResult
import os

def synthesize_ssml(payload, config=None):
    config = config or {}
    subscription_key = config.get('api_key', os.environ.get('AZURE_SPEECH_KEY'))
    region = config.get('region', os.environ.get('AZURE_SPEECH_REGION'))
    voice_name = payload.get('voice_name', config.get('voice', 'en-US-JennyNeural'))
    output_format = config.get('output_format', speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    client = AzureSpeechClient(subscription_key, region)
    synthesizer = client.get_speech_synthesizer(voice_name=voice_name, output_format=output_format)

    ssml_text = payload['ssml']
    result = synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure speech synthesis failed: {result.reason}. Error details: {result.error_details}")
    
    return AudioResult(result.audio_data, 'audio/mpeg')
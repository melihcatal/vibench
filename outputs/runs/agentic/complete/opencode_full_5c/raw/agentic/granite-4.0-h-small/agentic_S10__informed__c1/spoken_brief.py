# Later-step: generate spoken brief from model output
import os
from model_client import get_text_chat_client


def generate_spoken_brief(
    text: str, language: str = "en", model: str = "granite-4"
) -> bytes:
    """Synthesize speech from text using a text‑to‑speech service.

    Args:
        text: The generated model output to be spoken.
        language: Target language code (default: "en").
        model: Provider identifier (default: "granite-4").

    Returns:
        Raw audio bytes (e.g., mp3 or wav).
    """
    client = get_text_chat_client(model)

    # ----- Google Cloud Text-to-Speech -----
    if model == "google-tts":
        from google.cloud import texttospeech

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content

    # ----- IBM Watson Text‑to‑Speech -----
    if model == "ibm-watson-tts":
        from ibm_watson import TextToSpeechV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
        tts = TextToSpeechV1(authenticator=authenticator)
        tts.set_service_url(os.getenv("IBM_TTS_URL"))
        audio_format = "audio/wav" if language != "en" else "audio/mp3"
        response = tts.synthesize(
            text, accept=audio_format, voice="en-US_MichaelV3Voice"
        )
        return response.get_result().content

    # ----- Azure Speech Service -----
    if model == "azure-speech":
        from azure.cognitiveservices.speech import (
            SpeechConfig,
            AudioStreamFormat,
            AudioDataStream,
        )
        from azure.cognitiveservices.speech import SpeechSynthesizer

        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION")
        speech_config = SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        synthesizer = SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(text).get()
        return result.audio_data

    # ----- DashScope CosyVoice (audio) -----
    if model == "dashscope-cosyvoice":
        from dashscope import CosyVoiceClient

        client = CosyVoiceClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
        resp = client.synthesize(
            text=text, voice="default", sample_rate=24000, format="mp3"
        )
        return resp["audio"]

    # ----- ElevenLabs Text‑to‑Speech -----
    if model == "elevenlabs":
        import elevenlabs

        elevenlabs.api_key = os.getenv("ELEVENLABS_API_KEY")
        speech = elevenlabs.get_cloning_voice().generate_speech(
            text, voice_settings=elevenlabs.VoiceSettings()
        )
        return speech.content

    # ----- Amazon Polly -----
    if model == "amazon-polly":
        import boto3

        polly = boto3.client("polly")
        resp = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
        return resp["AudioStream"].read()

    raise ValueError(f"Unsupported TTS provider: {model}")


# Example (uncomment to test)
# audio = generate_spoken_brief("Welcome to the demo.", "es")
# with open('brief.mp3', 'wb') as f: f.write(audio)

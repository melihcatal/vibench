import boto3
import requests
import os
import elevenlabs


def generate_spoken_brief(text: str, provider: str = "google") -> bytes:
    """Synthesize spoken output from model brief text using a TTS service.

    Args:
        text (str): The text to convert to speech.
        provider (str): One of 'google', 'aws', 'dashscope', 'azure', 'elevenlabs'.

    Returns:
        bytes: Binary audio data ready to be saved or streamed.
    """
    if provider == "google":
        client = boto3.client("polly", region_name="us-east-1")
        response = client.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId="Joanna"
        )
        return response["AudioStream"].read()
    elif provider == "aws":
        # Amazon Polly (same client as above)
        return generate_spoken_brief(text, provider="google")
    elif provider == "azure":
        # Azure Speech TTS
        endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
        key = os.getenv("AZURE_SPEECH_KEY")
        headers = {"Ocp-Apim-Subscription-Key": key}
        payload = {
            "Input": {"text": text},
            "Voice": {"name": "en-US-JennyNeural", "gender": "female"},
        }
        r = requests.post(
            f"{endpoint}/speech/synthesize", headers=headers, json=payload
        )
        return r.content
    elif provider == "dashscope":
        client = dashscope.TextToSpeech(api_key=os.getenv("DASHSCOPE_API_KEY"))
        resp = client.tts(model="tts-speedy-neural", text=text, voice="alloy")
        return resp.audio_bytes
    elif provider == "elevenlabs":
        # ElevenLabs SDK
        client = elevenlabs.Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
        audio = client.text_to_speech(
            text, model_id="eleven_monolingual_v1", voice="CreepyCrisp"
        )
        return audio.content
    else:
        raise ValueError(f"Unsupported TTS provider: {provider}")

import boto3
import os

def generate_platform_brief_audio(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    """
    Generate audio using Amazon Polly.
    """
    polly = boto3.client("polly", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = polly.synthesize_speech(
        Text=text[:3000],  # Polly limit
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine="neural"
    )
    if "AudioStream" in response:
        audio_stream = response["AudioStream"]
        audio = audio_stream.read()
        audio_stream.close()
        return audio
    raise ValueError("Failed to synthesize speech")
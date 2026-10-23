import boto3
import os

def generate_audio_brief(text: str, output_format: str = "mp3", voice_id: str = "Joanna"):
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    polly_client = boto3.client('polly', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # In a real application, you'd save the audio stream to a file or return it directly.
    # For this example, we'll return a placeholder indicating success.
    if "AudioStream" in response:
        return f"Audio stream generated successfully for voice '{voice_id}'."
    else:
        return "Failed to generate audio stream."

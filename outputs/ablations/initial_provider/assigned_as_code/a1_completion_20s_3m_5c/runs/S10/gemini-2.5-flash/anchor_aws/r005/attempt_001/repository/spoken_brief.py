import boto3
import os


def generate_spoken_brief(payload, config=None):
    config = config or {}
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("polly", region_name=aws_region)

    text_to_speak = payload["text"]
    voice_id = payload.get("voice_id", "Joanna")  # Default to Joanna voice
    output_format = payload.get("output_format", "mp3")

    response = client.synthesize_speech(
        Text=text_to_speak,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # The audio stream is in response['AudioStream'].read()
    # In a real application, you'd save this to a file or stream it.
    # For this task, we'll return a placeholder indicating success and format.
    audio_stream_data = response["AudioStream"].read()

    # In a real scenario, you might save this to a temporary file or return a base64 encoded string
    # For this example, we'll return the length of the audio data and the format
    return {"audio_data_length": len(audio_stream_data), "output_format": output_format, "voice_id": voice_id}

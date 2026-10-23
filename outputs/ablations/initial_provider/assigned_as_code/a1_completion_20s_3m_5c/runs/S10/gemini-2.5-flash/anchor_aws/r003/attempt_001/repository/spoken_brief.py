import boto3
import os

def generate_spoken_brief(payload, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    client = boto3.client("polly", region_name=region)

    text_to_speak = payload.get("text", "")
    voice_id = payload.get("voice_id", "Joanna") # e.g., 'Joanna', 'Matthew', 'Amy'
    output_format = payload.get("output_format", "mp3") # e.g., 'mp3', 'ogg_vorbis', 'pcm'

    response = client.synthesize_speech(
        Text=text_to_speak,
        OutputFormat=output_format,
        VoiceId=voice_id,
    )

    # The audio stream is in response['AudioStream']
    # For this example, we'll return a placeholder or save to a temporary file.
    # In a real application, you'd stream this directly or save it.
    audio_stream = response["AudioStream"].read()

    # In a real scenario, you'd typically save this to a file or stream it.
    # For demonstration, we'll return a base64 encoded string or a direct byte stream reference.
    # Here, we'll just indicate success and some metadata.
    
    # Note: Directly returning a large audio_stream as part of a JSON response might not be ideal
    # for very large audio files due to response size limits. A common pattern is to upload it
    # to S3 and return a pre-signed URL.
    
    return {
        "message": "Audio stream generated successfully (not returned directly due to size).",
        "audio_length_bytes": len(audio_stream),
        "output_format": output_format,
        "voice_id": voice_id,
    }
